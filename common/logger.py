"""
Rotating file logger — consistent logging for all AeroHub modules.

Each module gets its own log file in the Logs/ directory with rotation.

Usage:
    from common.logger import get_logger
    log = get_logger("BatteryMonitor")
    log.info("Started")
    log.error("Something broke", exc_info=True)

Config is read from common/logger_config.json per module.
"""

import json
import logging
import os
from logging.handlers import RotatingFileHandler

# Resolve paths relative to project root (parent of common/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOGS_DIR = os.path.join(_PROJECT_ROOT, "Logs")
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logger_config.json")

_DEFAULT_CONFIG = {
    "level": "INFO",
    "max_bytes": 5_242_880,  # 5 MB
    "backup_count": 2,
    "console_output": True,
}


def _load_module_config(module_name: str) -> dict:
    """Load logger config for a specific module from central config file."""
    config = dict(_DEFAULT_CONFIG)
    try:
        if os.path.exists(_CONFIG_PATH):
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                all_config = json.load(f)
            if module_name in all_config:
                config.update(all_config[module_name])
    except (json.JSONDecodeError, OSError):
        pass
    return config


def get_logger(name: str) -> logging.Logger:
    """Create a rotating file logger for the given module name."""
    logger = logging.getLogger(f"AeroHub.{name}")

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    config = _load_module_config(name)
    logger.setLevel(getattr(logging, config["level"].upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler with rotation (with fallback if _LOGS_DIR is not writable)
    try:
        os.makedirs(_LOGS_DIR, exist_ok=True)
        log_file = os.path.join(_LOGS_DIR, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=config["max_bytes"],
            backupCount=config["backup_count"],
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, OSError):
        try:
            import tempfile
            fallback_dir = os.path.join(tempfile.gettempdir(), "aerohub_logs")
            os.makedirs(fallback_dir, exist_ok=True)
            fallback_file = os.path.join(fallback_dir, f"{name}.log")
            file_handler = RotatingFileHandler(
                fallback_file,
                maxBytes=config["max_bytes"],
                backupCount=config["backup_count"],
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass

    # Console handler (optional, useful for dev)
    if config.get("console_output", True):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
