import keyboard
from utils.logger import setup_logger

logger = setup_logger("keyboard")

class KeyboardController:
    def __init__(self, on_analyze, on_resume):
        self.on_analyze = on_analyze
        self.on_resume = on_resume

    def start(self):
        logger.info("Registering keyboard shortcuts")

        keyboard.add_hotkey(
            "ctrl+shift+enter",
            self._handle_analyze
        )

        keyboard.add_hotkey(
            "ctrl+shift+`",
            self._handle_resume
        )

    def _handle_analyze(self):
        logger.info("Ctrl+Shift+Enter pressed → Analyze trigger")
        self.on_analyze()

    def _handle_resume(self):
        logger.info("Ctrl+Shift+` pressed → Resume capture trigger")
        self.on_resume()
