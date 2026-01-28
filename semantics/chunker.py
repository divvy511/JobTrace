import time
from utils.logger import setup_logger
import config

logger = setup_logger("chunker")

class SemanticChunker:
    def __init__(self):
        self.chunk_start_time = time.time()

    def should_close_chunk(self) -> bool:
        return (time.time() - self.chunk_start_time) > config.CHUNK_TIME_LIMIT_SECONDS

    def reset(self):
        self.chunk_start_time = time.time()
