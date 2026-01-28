from storage.db import init_db
from utils.logger import setup_logger

logger = setup_logger("timeline")

def persist_action(action):
    init_db()
    # insert logic here (kept simple for now)
