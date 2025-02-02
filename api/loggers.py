import sys
import os
import logging

class LoggerWriter:
    """Redirects all print() to the logger"""
    def write(self, message):
        if message.strip():
            logging.info(message.strip())

    def flush(self):
        pass

def init_logging(prefix: str):
    LOG_FILE = os.path.join(prefix, "pipeline.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    sys.stdout = LoggerWriter()

def get_logger():
    return logging.getLogger()
