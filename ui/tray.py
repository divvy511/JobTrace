from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QPoint, QTimer, Slot

from ui.panel import ControlPanel
from core.state import AppState

if TYPE_CHECKING:
    from PySide6.QtWidgets import QApplication
    from typing import Any

logger = logging.getLogger(__name__)


class TrayController:
    def __init__(self, app: QApplication, engine: Any):
        self.app = app
        self.engine = engine

        self.icons = self._load_icons()
        self.tray = QSystemTrayIcon(self.icons[AppState.WAITING], app)

        menu = QMenu()
        exit_action = QAction("Exit JobTrace", menu)
        exit_action.triggered.connect(self._exit)
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_click)

        self.panel = ControlPanel(engine)
        self.tray.show()

        self._last_state = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._sync_state)
        self._timer.start(400)

        engine.on_analysis_complete = self._notify_success
        engine.on_analysis_error = self._notify_error

    def _load_icons(self):
        base = Path(__file__).parent / "icons"
        return {
            AppState.CAPTURING: QIcon(str(base / "tray_green.png")),
            AppState.ANALYZING: QIcon(str(base / "tray_blue.png")),
            AppState.WAITING: QIcon(str(base / "tray_yellow.png")),
            AppState.ERROR: QIcon(str(base / "tray_red.png")),
        }

    @Slot(QSystemTrayIcon.ActivationReason)
    def _on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            pos = self.tray.geometry().topLeft()
            self.panel.update_status()
            self.panel.show_with_animation(QPoint(pos.x() - 260, pos.y() - 180))

    def _sync_state(self):
        state = self.engine.get_state()
        if state != self._last_state:
            self.tray.setIcon(self.icons.get(state))
            self.tray.setToolTip(f"JobTrace – {state.value}")
            self._last_state = state

    def _exit(self):
        self.engine.shutdown()
        self.tray.hide()
        self.app.quit()

    def _notify_success(self, count: int):
        self.tray.showMessage(
            "JobTrace",
            f"Analysis complete. {count} action(s) recorded.",
            QSystemTrayIcon.Information,
            3000,
        )

    def _notify_error(self, msg: str):
        self.tray.showMessage(
            "JobTrace – Error",
            msg,
            QSystemTrayIcon.Critical,
            4000,
        )
