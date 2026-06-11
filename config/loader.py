import os
import re
import json
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]+))?\}")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "app.yaml"
ENV_PATH = REPO_ROOT / ".env"


def _expand_value(value: str) -> str:
    if not isinstance(value, str):
        return value

    def repl(match):
        name = match.group(1)
        default = match.group(2)
        return os.getenv(name, default if default is not None else "")

    return ENV_PATTERN.sub(repl, value)


def _expand(obj):
    if isinstance(obj, dict):
        return {k: _expand(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_expand(v) for v in obj]
    if isinstance(obj, str):
        return _expand_value(obj)
    return obj


def load_env(path: Path | str = None) -> dict:
    path = Path(path or ENV_PATH)
    env = {}
    if not path.exists():
        return env

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise ImportError("PyYAML is required to load YAML configuration")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_config(path: Path | str = None) -> dict:
    path = Path(path or DEFAULT_CONFIG_PATH)
    config: dict = {}
    if path.exists():
        if path.suffix in {".yaml", ".yml"}:
            config = _load_yaml(path)
        elif path.suffix == ".json":
            config = _load_json(path)
    env_config = load_env(path=ENV_PATH)
    # Set environment vars as overrides
    for key, value in env_config.items():
        if key.isupper():
            parts = key.lower().split("__")
            target = config
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = _expand_value(value)
    return _expand(config)


def get_runtime_option(key: str, default=None):
    config = load_config()
    parts = key.split(".")
    node = config
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node


def expand_env(obj):
    """Public helper to expand environment variables in a data structure.

    Accepts a mapping, sequence, or string and returns a new object with
    ${VAR} placeholders replaced from the environment.
    """
    return _expand(obj)
