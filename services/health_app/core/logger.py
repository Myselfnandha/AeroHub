import os
import sys
import logging
import logging.handlers

# Resolve paths relative to app root
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(os.path.dirname(APP_ROOT), "Logs")
LOG_PATH = os.path.join(LOGS_DIR, "health_app.log")

os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HealthApp")

# Suppress noisy EDID parse warnings from screen_brightness_control
logging.getLogger("screen_brightness_control").setLevel(logging.ERROR)
