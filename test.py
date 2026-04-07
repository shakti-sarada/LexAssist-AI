import os
import logging

# 🔥 Create logs folder
os.makedirs("logs", exist_ok=True)

# 🔥 Create logger
logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)

# 🔥 Avoid duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler("logs/test.log", mode="a")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# 🔥 TEST LOGS
logger.info("Logging test started")
logger.warning("This is a warning log")
logger.error("This is an error log")

print("\nCheck logs/test.log file\n")