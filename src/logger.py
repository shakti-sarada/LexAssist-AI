import os
import logging

# Create logs folder
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("rag_logger")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers
if not logger.handlers:

    file_handler = logging.FileHandler("logs/rag_system.log", mode="a")
    file_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)