import logging #Python's built-in logging library.
from pathlib import Path

Path("reports/logs").mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("Playwright")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("reports/logs/test.log", mode="w")
    formatter = logging.Formatter("%(asctime)s || %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)






