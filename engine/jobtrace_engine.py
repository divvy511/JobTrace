import time
import threading
import uuid
from capture.screen_sampler import ScreenSampler
from capture.buffer import FrameBuffer
from llm.gemini_client import GeminiClient
from sheets.sheets_client import SheetsClient
from llm.parser import extract_json
from llm.validator import validate_actions
from core.state import AppState
from utils.logger import setup_logger

logger = setup_logger("engine")


class JobTraceEngine:
    def __init__(self, capture_interval_sec: int = 3):
        self.capture_interval = capture_interval_sec

        self.sampler = ScreenSampler()
        self.buffer = FrameBuffer()
        self.gemini = GeminiClient()
        self.sheets = SheetsClient()

        self.state = AppState.WAITING
        self._stop_event = threading.Event()
        self._capture_thread: threading.Thread | None = None
        self._lock = threading.Lock()

        self.on_analysis_complete = None
        self.on_analysis_error = None

        logger.info("JobTraceEngine initialized")

    # -----------------------------
    # Lifecycle
    # -----------------------------
    def start(self):
        with self._lock:
            if self.state == AppState.CAPTURING:
                logger.info("Engine already capturing")
                return

            self.state = AppState.CAPTURING
            self._stop_event.clear()

            self._capture_thread = threading.Thread(
                target=self._capture_loop, daemon=True
            )
            self._capture_thread.start()

            logger.info("Engine started → CAPTURING")

    def pause(self):
        with self._lock:
            if self.state != AppState.CAPTURING:
                logger.info("Pause ignored (not capturing)")
                return

            self.state = AppState.WAITING
            logger.info("Engine paused → WAITING")

    def resume(self):
        with self._lock:
            if self.state != AppState.WAITING:
                logger.info("Resume ignored (not waiting)")
                return

            self.state = AppState.CAPTURING
            logger.info("Engine resumed → CAPTURING")

    def shutdown(self):
        logger.info("Engine shutdown requested")

        self._stop_event.set()

        if self._capture_thread and self._capture_thread.is_alive():
            self._capture_thread.join(timeout=5)

        self.state = AppState.WAITING
        logger.info("Engine stopped")

    # -----------------------------
    # Capture Loop
    # -----------------------------
    def _capture_loop(self):
        logger.info("Capture loop started")

        while not self._stop_event.is_set():
            if self.state == AppState.CAPTURING:
                try:
                    frame = self.sampler.capture_frame()
                    self.buffer.add_frame(frame)
                except Exception as e:
                    logger.error(f"Frame capture failed: {e}", exc_info=True)

            time.sleep(self.capture_interval)

        logger.info("Capture loop exited")

    # -----------------------------
    # Analyze
    # -----------------------------
    def analyze(self):
        with self._lock:
            if self.state != AppState.CAPTURING:
                logger.info("Analyze ignored (engine not in CAPTURING state)")
                return

            self.state = AppState.ANALYZING

        session_id = str(uuid.uuid4())
        frames = self.buffer.get_all()

        logger.info(f"[session={session_id}] Analyze started with {len(frames)} frames")

        try:
            gemini_text = self.gemini.analyze_frames(frames, session_id=session_id)

            raw = extract_json(gemini_text)
            actions = validate_actions(raw)

            self.sheets.append_job_actions(actions)

            logger.info(f"[session={session_id}] Analysis written to Sheets")

            if self.on_analysis_complete:
                self.on_analysis_complete(len(actions))

        except Exception as e:
            logger.error(f"[session={session_id}] Analyze failed", exc_info=True)

            if self.on_analysis_error:
                self.on_analysis_error(str(e))

        finally:
            self.buffer.clear()
            self.state = AppState.WAITING

            logger.info(f"[session={session_id}] Engine state → WAITING")

    # -----------------------------
    # Session Control
    # -----------------------------
    def new_session(self):
        with self._lock:
            logger.info("New session requested")

            self.buffer.clear()
            self._stop_event.clear()

            if not self._capture_thread or not self._capture_thread.is_alive():
                self._capture_thread = threading.Thread(
                    target=self._capture_loop, daemon=True
                )
                self._capture_thread.start()
                logger.info("Capture thread started")

            self.state = AppState.CAPTURING
            logger.info("New session started → CAPTURING")

    # -----------------------------
    # State
    # -----------------------------
    def get_state(self) -> AppState:
        return self.state
