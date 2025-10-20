import logging
import sys

# ANSI color codes
COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[37m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[41m",
    "RESET": "\033[0m"
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, "")
        reset = COLORS["RESET"]
        message = super().format(record)
        return f"{color}{message}{reset}"

# Expose app logger
logger = logging.getLogger("waterlevel.main")

def setup_logging():
    # 🔥 Clear all handlers from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # ✅ App logger to console with color
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.propagate = False

    # 🔇 Suppress noisy logs
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    # ✅ SQLAlchemy logs to file only
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)
    sql_logger.handlers.clear()

    sql_file_handler = logging.FileHandler("sqlalchemy.log", mode="a", encoding="utf-8")
    sql_file_handler.setFormatter(logging.Formatter("[SQL] %(asctime)s - %(message)s"))

    sql_logger.addHandler(sql_file_handler)
    sql_logger.propagate = False  # 🔒 Prevent console output