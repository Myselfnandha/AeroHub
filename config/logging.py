import json
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

try:
    import sentry_sdk
except ImportError:  # pragma: no cover
    sentry_sdk = None


class JsonFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        extra = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
        }
        if record.exc_info:
            extra["exception"] = self.formatException(record.exc_info)
        return json.dumps(extra, ensure_ascii=False)


def setup_logging(app_name: str = "app", config: dict | None = None):
    config = config or {}
    root = logging.getLogger()
    if root.handlers:
        return root

    log_settings = config.get("logging", {})
    log_dir = Path(log_settings.get("path", "Logs"))
    log_file = log_settings.get("file", f"{app_name}.log")
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, log_settings.get("level", "INFO").upper(), logging.INFO)
    formatter = JsonFormatter()

    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(stream)

    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=int(log_settings.get("max_bytes", 5 * 1024 * 1024)),
        backupCount=int(log_settings.get("backup_count", 3)),
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    root.setLevel(level)

    if config.get("sentry", {}).get("enabled"):
        dsn = config.get("sentry", {}).get("dsn") or os.getenv("SENTRY_DSN")
        if dsn and sentry_sdk is not None:
            sentry_sdk.init(dsn=dsn, release=os.getenv("GITHUB_SHA"), environment=os.getenv("ENV", "dev"))
            root.info("Sentry integration enabled.")
        elif config.get("sentry", {}).get("enabled"):
            root.warning("Sentry enabled in config, but sentry-sdk is not installed.")

    return root
