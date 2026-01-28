from mss import mss
from PIL import Image
from utils.logger import setup_logger

logger = setup_logger("screen_sampler")


class ScreenSampler:
    def __init__(self):
        self._sct = None
        self._monitor = None

    def _ensure_context(self):
        """
        Ensure MSS is initialized in the CURRENT thread.
        """
        if self._sct is None:
            self._sct = mss()
            self._monitor = self._sct.monitors[1]
            logger.info("MSS context initialized in capture thread")

    def capture_frame(self) -> Image.Image:
        try:
            self._ensure_context()

            screenshot = self._sct.grab(self._monitor)

            img = Image.frombytes(
                "RGB",
                (screenshot.width, screenshot.height),
                screenshot.rgb,
            )

            return img

        except Exception as e:
            logger.error(f"Screen capture failed: {e}", exc_info=True)
            raise
