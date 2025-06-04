import os
import sys
from datetime import datetime

from loguru import logger

# Remove default logger to avoid double logs
logger.remove()

# Create a log directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Log filename format
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Console logger
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)

# File logger
logger.add(
    log_file,
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    encoding="utf-8",
    enqueue=True,
)

# Exportable logger
log = logger
