import sys
from PySide6.QtWidgets import QApplication
from engine.jobtrace_engine import JobTraceEngine
from core.keyboard_listener import KeyboardController
from ui.tray import TrayController
from utils.logger import setup_logger


logger = setup_logger("main")


def main():
    app = QApplication(sys.argv)

    engine = JobTraceEngine()
    #engine.start()

    keyboard = KeyboardController(
        on_analyze=engine.analyze, on_resume=engine.new_session
    )
    keyboard.start()

    tray = TrayController(app, engine)

    logger.info("JobTrace UI started")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
