import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger("daft_bot")


def setup_logging(
    log_file: str = "daft_bot.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 3,
) -> None:
    """
    Configure logging for the application.

    Logs to both console and file with rotation.
    """
    logger.setLevel(level)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return

    # Format: timestamp - level - message
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler - shows INFO and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler - logs everything with rotation
    log_path = Path(log_file)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance. Uses child logger if name provided."""
    if name:
        return logger.getChild(name)
    return logger
