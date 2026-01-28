from pathlib import Path

BASE_DIR = Path(__file__).parent

TEMP_FRAME_DIR = BASE_DIR / "temp" / "frames"
TEMP_FRAME_DIR.mkdir(parents=True, exist_ok=True)

SCREEN_SAMPLING_INTERVAL_SECONDS = 3
MAX_BUFFER_FRAMES = 120  # ~6 minutes at 3s sampling

FRAME_MAX_WIDTH = 1280

GEMINI_VISION_MODEL = "gemini-2.5-flash"
GEMINI_TEXT_MODEL = "gemini-2.5-flash"


DATABASE_PATH = BASE_DIR / "jobtrace.db"

CHUNK_TIME_LIMIT_SECONDS = 300  # 5 minutes
