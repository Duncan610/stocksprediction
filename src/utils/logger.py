import logging
import os
from datetime import datetime

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    log_file = log_file or f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    log_file_path = os.path.join(os.getcwd(), "logs", log_file)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger(__name__)  # This defines the 'logger' object

if __name__ == "__main__":
    logger.info("Logging has started")