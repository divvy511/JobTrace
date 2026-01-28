from enum import Enum


class AppState(Enum):
    CAPTURING = "CAPTURING"
    ANALYZING = "ANALYZING"
    WAITING = "WAITING"
    ERROR = "ERROR"
