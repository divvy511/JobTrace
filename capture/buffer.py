from collections import deque
from pathlib import Path
from utils.logger import setup_logger
import config

logger = setup_logger("buffer")

class FrameBuffer:
    def __init__(self):
        self.frames = deque(maxlen=config.MAX_BUFFER_FRAMES)

    def add_frame(self, frame_path: Path):
        self.frames.append(frame_path)
        logger.info(f"Frame added (buffer size={len(self.frames)})")

    def get_all(self) -> list[Path]:
        return list(self.frames)

    def clear(self):
        logger.info("Clearing frame buffer and deleting frames")
        for frame in self.frames:
            try:
                frame.unlink(missing_ok=True)
            except Exception:
                pass
        self.frames.clear()
