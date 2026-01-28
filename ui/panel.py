"""
Control panel widget with smooth animations and modern styling.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, Slot
from PySide6.QtGui import QColor

from core.state import AppState

if TYPE_CHECKING:
    from typing import Any

logger = logging.getLogger(__name__)


class ControlPanel(QWidget):
    """
    Popup control panel for JobTrace application.
    """

    # Optimized dimensions
    PANEL_WIDTH = 280
    PANEL_HEIGHT = 195

    ANIMATION_DURATION_MS = 180
    SHADOW_BLUR_RADIUS = 40
    SHADOW_OFFSET_Y = 10

    def __init__(self, engine: Any) -> None:
        super().__init__()

        self.engine = engine

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Popup
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_ui()
        self._setup_animation()

        logger.debug("ControlPanel initialized")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        container = QWidget(self)
        container.setObjectName("container")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(0)

        # Header
        self._title_label = QLabel()
        self._title_label.setObjectName("title")

        self._status_label = QLabel("Status: WAITING")
        self._status_label.setObjectName("status")

        # Buttons
        self._start_btn = QPushButton("Start / New Session")
        self._start_btn.setObjectName("primaryButton")
        self._start_btn.clicked.connect(self._on_start_clicked)

        self._pause_btn = QPushButton("Pause")
        self._pause_btn.clicked.connect(self._on_pause_clicked)

        self._analyze_btn = QPushButton("Analyze Task")
        self._analyze_btn.clicked.connect(self._on_analyze_clicked)

        layout.addWidget(self._title_label)
        layout.addSpacing(4)
        layout.addWidget(self._status_label)
        layout.addSpacing(6)
        layout.addWidget(self._start_btn)
        layout.addSpacing(6)
        layout.addWidget(self._pause_btn)
        layout.addSpacing(6)
        layout.addWidget(self._analyze_btn)

        # Enhanced shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(self.SHADOW_BLUR_RADIUS)
        shadow.setOffset(0, self.SHADOW_OFFSET_Y)
        shadow.setColor(QColor(0, 0, 0, 180))
        container.setGraphicsEffect(shadow)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(container)

        self._apply_stylesheet()
        self.setFixedSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)

        # Initial state paint
        self.update_status()

    # ------------------------------------------------------------------
    # Styling - MUCH IMPROVED
    # ------------------------------------------------------------------
    def _apply_stylesheet(self) -> None:
        self.setStyleSheet("""
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            }
            
            #container {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(24, 24, 27, 0.98),
                    stop:1 rgba(18, 18, 20, 0.98)
                );
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            #title {
                font-size: 15px;
                font-weight: 600;
                color: #fafafa;
                letter-spacing: -0.3px;
                padding-bottom: 2px;
            }

            #status {
                font-size: 11px;
                color: #a1a1aa;
                font-weight: 500;
                letter-spacing: 0.2px;
                padding-bottom: 4px;
            }

            QPushButton {
                min-height: 26px;
                max-height: 30px;
                background-color: rgba(63, 63, 70, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 7px;
                padding: 5px 12px;
                color: #e4e4e7;
                font-size: 13px;
                font-weight: 500;
                letter-spacing: -0.1px;
            }

            QPushButton:hover {
                background-color: rgba(82, 82, 91, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            QPushButton:pressed {
                background-color: rgba(39, 39, 42, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.03);
            }
            
            QPushButton:disabled {
                background-color: rgba(39, 39, 42, 0.7);
                color: #71717a;
                border: 1px solid rgba(255, 255, 255, 0.02);
            }

            #primaryButton {
                background-color: rgba(59, 130, 246, 0.85);
                border: 1px solid rgba(96, 165, 250, 0.3);
                color: #ffffff;
                font-weight: 600;
            }

            #primaryButton:hover {
                background-color: rgba(59, 130, 246, 1.0);
                border: 1px solid rgba(96, 165, 250, 0.5);
            }

            #primaryButton:pressed {
                background-color: rgba(37, 99, 235, 1.0);
                border: 1px solid rgba(59, 130, 246, 0.5);
            }
        """)

    # ------------------------------------------------------------------
    # Animation
    # ------------------------------------------------------------------
    def _setup_animation(self) -> None:
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(self.ANIMATION_DURATION_MS)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def show_with_animation(self, position: QPoint) -> None:
        self.move(position)
        self.setWindowOpacity(0.0)
        self.show()
        self._fade_anim.start()

    # ------------------------------------------------------------------
    # Status & header dot logic
    # ------------------------------------------------------------------
    def update_status(self) -> None:
        try:
            state = self.engine.get_state()
            self._status_label.setText(f"Status: {state.value}")
            self._update_title_dot(state)
        except Exception:
            self._status_label.setText("Status: ERROR")
            self._update_title_dot(AppState.ERROR)

    def _update_title_dot(self, state: AppState) -> None:
        color_map = {
            AppState.CAPTURING: "#10b981",  # green
            AppState.ANALYZING: "#3b82f6",  # blue
            AppState.WAITING: "#fbbf24",  # amber (more visible)
            AppState.ERROR: "#ef4444",  # red
        }

        color = color_map.get(state, "#a1a1aa")

        # Use a slightly larger, more visible dot with better rendering
        self._title_label.setText(
            f'<span style="color:{color}; font-size:16px; line-height:1;">●</span> '
            f'<span style="color:#fafafa;">JobTrace</span>'
        )

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------
    @Slot()
    def _on_start_clicked(self) -> None:
        self.engine.new_session()
        self._pause_btn.setText("Pause")
        self.update_status()

    @Slot()
    def _on_pause_clicked(self) -> None:
        state = self.engine.get_state()

        if state == AppState.CAPTURING:
            self.engine.pause()
            self._pause_btn.setText("Resume")
        else:
            self.engine.resume()
            self._pause_btn.setText("Pause")

        self.update_status()

    @Slot()
    def _on_analyze_clicked(self) -> None:
        self.engine.analyze()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def hideEvent(self, event) -> None:
        self._pause_btn.setText("Pause")
        super().hideEvent(event)
