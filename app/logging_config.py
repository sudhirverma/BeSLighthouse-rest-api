import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from .config import config

def configure_logging(app: Flask) -> None:
    """Configure root and app logger with console + rotating file handlers."""
    # Root logger configuration
    log_dir = config.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'beslighthouse.log')

    # Determine level
    level = logging.INFO if config.ENV == 'production' else logging.DEBUG

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')

    # Console handler (stdout)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(level)

    # Rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=7)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Configure root logger
    root = logging.getLogger()
    # avoid adding duplicate handlers in interactive environments
    if not root.handlers:
        root.setLevel(level)
        root.addHandler(console)
        root.addHandler(file_handler)

    # Flask app logger uses root handlers but set level explicitly
    app.logger.setLevel(level)
