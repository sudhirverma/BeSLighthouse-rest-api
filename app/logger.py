import logging
import logging.handlers
import os

def setup_logging():
    logger = logging.getLogger("besl_app")
    if logger.handlers:
        return logger

    level = os.getenv("BESL_LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("BESL_LOG_FILE", "logs/besl_app.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger
