# ruff: noqa: E402
import os
import re
import asyncio
import json
import io
import sys
import socket
import logging
import logging.handlers
import subprocess
import time
import threading
import tkinter as tk

# Force UTF-8 output on Windows console to avoid emoji encoding crashes
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from aiohttp import web
from telethon import TelegramClient, events, Button, utils
from telethon.tl.functions.bots import SetBotCommandsRequest
from telethon.tl.types import (
    BotCommand,
    BotCommandScopeDefault,
    KeyboardButtonRequestPeer,
    RequestPeerTypeBroadcast,
    ReplyKeyboardMarkup,
    KeyboardButtonRow,
    MessageActionRequestedPeerSentMe,
    RequestedPeerChannel,
    PeerChannel,
)
from dotenv import load_dotenv

try:
    import pystray
    from PIL import Image, ImageDraw

    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes as _ctypes

    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.TgFdmProxy")
except Exception:
    pass


# ────────────────────────────────────────────────────────
#  Environment — interactive setup wizard (from tg_fdm_proxy 1.py)
# ────────────────────────────────────────────────────────
def ensure_env():
    """Check .env for credentials; prompt interactively if any are missing."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)

    api_id = os.getenv("API_ID", "").strip()
    api_hash = os.getenv("API_HASH", "").strip()
    bot_token = os.getenv("BOT_TOKEN", "").strip()

    if not all([api_id, api_hash, bot_token]):
        print("\n" + "=" * 50)
        print("  TELEGRAM FDM PROXY - FIRST-TIME SETUP")
        print("=" * 50)
        print("Get these values from https://my.telegram.org and @BotFather\n")
        try:
            if not api_id:
                api_id = input("1. Enter your API_ID   : ").strip()
            if not api_hash:
                api_hash = input("2. Enter your API_HASH : ").strip()
            if not bot_token:
                bot_token = input("3. Enter your BOT_TOKEN: ").strip()

            with open(env_path, "w") as f:
                f.write(f"API_ID={api_id}\n")
                f.write(f"API_HASH={api_hash}\n")
                f.write(f"BOT_TOKEN={bot_token}\n")

            print(f"\nConfiguration saved to: {env_path}")
            load_dotenv(env_path)
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(1)

    return api_id, api_hash, bot_token


def save_config_to_env(new_config: dict) -> bool:
    """Write config dict back to .env file, preserving other lines/comments."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    lines = []
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            logger.error(f"[CONFIG] Failed to read .env for saving: {e}")
            return False

    key_line_index = {}
    for i, line in enumerate(lines):
        clean = line.strip()
        if "=" in clean and not clean.startswith("#"):
            k = clean.split("=", 1)[0].strip()
            key_line_index[k] = i

    for k, v in new_config.items():
        val_str = str(v)
        if k in key_line_index:
            idx = key_line_index[k]
            orig_line = lines[idx]
            eq_idx = orig_line.find("=")
            hash_idx = orig_line.find("#", eq_idx)
            if hash_idx != -1:
                comment = orig_line[hash_idx:]
                lines[idx] = f"{k}={val_str}   {comment.lstrip(' \t')}"
            else:
                lines[idx] = f"{k}={val_str}\n"
        else:
            if lines and not lines[-1].endswith("\n"):
                lines[-1] = lines[-1] + "\n"
            lines.append(f"{k}={val_str}\n")
            key_line_index[k] = len(lines) - 1

    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        logger.info(f"[CONFIG] Saved settings to .env: {new_config}")
        return True
    except Exception as e:
        logger.error(f"[CONFIG] Failed to write settings to .env: {e}")
        return False


API_ID, API_HASH, BOT_TOKEN = ensure_env()
API_ID = int(API_ID)

# Target Channels (optional)
raw_channels = os.getenv("TARGET_CHANNELS", "").strip()
TARGET_CHANNELS = []
if raw_channels:
    for c in raw_channels.split(","):
        c = c.strip()
        if c.isdigit() or (c.startswith("-") and c[1:].isdigit()):
            TARGET_CHANNELS.append(int(c))
        elif c:
            TARGET_CHANNELS.append(c)

MIN_FILE_SIZE_MB = float(os.getenv("MIN_FILE_SIZE_MB", "50").strip())
# How long (seconds) to wait for more quality variants before picking the best
QUALITY_WAIT_SECS = int(os.getenv("QUALITY_WAIT_SECS", "30").strip())

# Option G: allowed file-extension filter — empty = accept everything
_raw_ext = os.getenv("ALLOWED_EXT", "").strip()
ALLOWED_EXT: set[str] = set()
if _raw_ext:
    for _e in _raw_ext.split(","):
        _e = _e.strip().lower()
        ALLOWED_EXT.add(_e if _e.startswith(".") else f".{_e}")

PROXY_HOST = os.getenv("PROXY_HOST", "127.0.0.1")
PROXY_PORT = int(os.getenv("PROXY_PORT", "8080"))
DOWNLOAD_METHOD = os.getenv("DOWNLOAD_METHOD", "sequential").strip().lower()

def detect_openvpn_gui() -> str:
    """Scan Windows registry and common fallback paths for openvpn-gui.exe."""
    try:
        import winreg
        hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
        subkeys = [
            r"SOFTWARE\OpenVPN",
            r"SOFTWARE\Wow6432Node\OpenVPN",
            r"SOFTWARE\OpenVPN-GUI",
            r"SOFTWARE\Wow6432Node\OpenVPN-GUI"
        ]
        for hive in hives:
            for subkey in subkeys:
                try:
                    with winreg.OpenKey(hive, subkey) as key:
                        for val_name in ("", "exe_path", "config_dir", "log_dir"):
                            try:
                                val, _ = winreg.QueryValueEx(key, val_name)
                                if val:
                                    if os.path.isfile(val) and "openvpn" in val.lower():
                                        dir_path = os.path.dirname(val)
                                        candidate = os.path.join(dir_path, "openvpn-gui.exe")
                                        if os.path.isfile(candidate):
                                            return candidate
                                    elif os.path.isdir(val):
                                        for sub in ("", "bin"):
                                            candidate = os.path.join(val, sub, "openvpn-gui.exe")
                                            if os.path.isfile(candidate):
                                                return candidate
                                            parent = os.path.dirname(val)
                                            candidate = os.path.join(parent, "bin", "openvpn-gui.exe")
                                            if os.path.isfile(candidate):
                                                return candidate
                            except FileNotFoundError:
                                pass
                except Exception:
                    pass
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["where", "openvpn-gui.exe"],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode == 0:
            first_line = result.stdout.strip().splitlines()[0].strip()
            if os.path.isfile(first_line):
                return first_line
    except Exception:
        pass

    fallbacks = [
        r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe",
        r"C:\Program Files (x86)\OpenVPN\bin\openvpn-gui.exe",
    ]
    for fb in fallbacks:
        if os.path.isfile(fb):
            return fb

    return r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"


OPENVPN_GUI_PATH = os.getenv("OPENVPN_GUI_PATH", "").strip()
if not OPENVPN_GUI_PATH:
    OPENVPN_GUI_PATH = detect_openvpn_gui()

OPENVPN_PROFILE_TYPE = os.getenv("OPENVPN_PROFILE_TYPE", "US Free").strip()
OPENVPN_CONFIG_NAME = os.getenv("OPENVPN_CONFIG_NAME", "").strip()
VPN_TOGGLE = os.getenv("VPN_TOGGLE", "False").strip().lower() == "true"


def get_download_folder():
    try:
        import winreg

        sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
    except Exception:
        return os.path.join(os.path.expanduser("~"), "Downloads")


DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "").strip()
if not DOWNLOAD_DIR:
    DOWNLOAD_DIR = get_download_folder()


# Option P: keyword filters — comma-separated, case-insensitive
def _kw_set(env_key: str) -> set[str]:
    raw = os.getenv(env_key, "").strip()
    return {w.strip().lower() for w in raw.split(",") if w.strip()} if raw else set()


KEYWORD_BLOCK = _kw_set("KEYWORD_BLOCK")  # e.g. sample,trailer,cam,ts
KEYWORD_ALLOW = _kw_set("KEYWORD_ALLOW")  # e.g. 1080p,bluray,webrip  (empty=allow all)

# Option O: duplicate guard — (chat_id, message_id) → timestamp triggered
_triggered: dict[tuple, float] = {}
TRIGGER_TTL_SECS = 3600  # forget entries after 1 hour


def _is_duplicate(chat_id: int, message_id: int) -> bool:
    key = (chat_id, message_id)
    now = time.monotonic()
    # Prune stale entries
    stale = [k for k, t in _triggered.items() if now - t > TRIGGER_TTL_SECS]
    for k in stale:
        del _triggered[k]
    if key in _triggered:
        return True
    _triggered[key] = now
    return False


# Option S: auto-rename — clean filename for FDM/library
_NOISE_RE = re.compile(
    r"[\._\-\s]+("
    r"hdrip|bdrip|bluray|blu-ray|webrip|web-dl|web|hdtv|dvdrip|hq"
    r"|x264|x265|hevc|avc|xvid|divx"
    r"|aac|ac3|eac3|dd\d|dts|atmos|mp3"
    r"|esub|subs?|sub"
    r"|multi|dual|hindi|tamil|telugu|english|dubbed"
    r"|\@[\w]+"
    r")(?=[\._\-\s]|$)",
    re.IGNORECASE,
)
_RES_RE = re.compile(r"(2160p?|4k|uhd|1080p?|720p?|480p?|360p?)", re.IGNORECASE)
_YEAR_RE = re.compile(r"(?<![\d])(19\d{2}|20[0-2]\d)(?![\d])")


def auto_rename(raw: str) -> str:
    """Option S: format raw filename as 'Title (Year) [Resolution].ext'."""
    ext = os.path.splitext(raw)[1]  # keep original extension
    stem = os.path.splitext(raw)[0]

    res_m = _RES_RE.search(stem)
    year_m = _YEAR_RE.search(stem)
    res = res_m.group(1).upper() if res_m else ""
    year = year_m.group(1) if year_m else ""

    # Remove resolution and year in descending index order to avoid index shift issues
    slices = []
    if res_m:
        slices.append((res_m.start(), res_m.end()))
    if year_m:
        slices.append((year_m.start(), year_m.end()))

    slices.sort(key=lambda s: s[0], reverse=True)

    title = stem
    for start_idx, end_idx in slices:
        title = title[:start_idx] + " " + title[end_idx:]

    # Remove noise tokens
    title = _NOISE_RE.sub(" ", title)
    # Collapse separators to spaces
    title = re.sub(r"[\._\-]+", " ", title).strip()
    title = re.sub(r"\s{2,}", " ", title)

    if not title:
        return raw  # bail — couldn't parse anything useful

    parts = [title]
    if year:
        parts.append(f"({year})")
    if res:
        parts.append(f"[{res}]")
    return " ".join(parts) + ext


def find_free_port(start: int = 8080, max_attempts: int = 100) -> int:
    """Find an available TCP port starting from `start` (from tg_fdm_proxy 1.py)."""
    for port in range(start, start + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        f"No free ports found between {start} and {start + max_attempts - 1}"
    )


# ────────────────────────────────────────────────────────
#  Logging
# ────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
LOG_FILE_PATH = os.path.join(ROOT_DIR, "tg_fdm_proxy.log")

# Ensure workspace root is in sys.path to import services.aerohub_core.system_utils as system_utils
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(ROOT_DIR))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
import services.aerohub_core.system_utils as system_utils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024,  # 5 MB per file
            backupCount=3,
            encoding="utf-8",
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
# Silence Telethon's verbose flood-wait / chunk progress spam
logging.getLogger("telethon").setLevel(logging.WARNING)

# ────────────────────────────────────────────────────────
#  Event Log System (In-Memory structured events for GUI)
# ────────────────────────────────────────────────────────
EVENT_LOG = []
EVENT_LOG_LOCK = threading.Lock()


def add_event(category: str, message: str, level: str = "info"):
    timestamp = time.strftime("%H:%M:%S")
    event = {
        "time": timestamp,
        "category": category,
        "message": message,
        "level": level.lower(),
    }
    with EVENT_LOG_LOCK:
        EVENT_LOG.append(event)
        if len(EVENT_LOG) > 500:
            EVENT_LOG.pop(0)

    # Send dynamically to running LogDashboard
    if LogDashboard._instance and LogDashboard._instance.running:
        try:
            LogDashboard._instance.queue.put(
                (
                    LogDashboard._instance._add_event_to_ui,
                    (timestamp, category, message, level.lower()),
                )
            )
        except Exception:
            pass


# ────────────────────────────────────────────────────────
#  Download Manager Detection  (dynamic — registry first)
# ────────────────────────────────────────────────────────

# Known exe filenames per manager ID
MANAGER_EXE_NAMES = {
    "fdm": "fdm.exe",
    "idm": "IDMan.exe",
    "neat": "NeatDM.exe",
}

# CLI command templates per manager ({ exe } and { url } are substituted at call time)
MANAGER_COMMANDS = {
    "fdm": ["{exe}", "-a", "{url}"],
    "idm": ["{exe}", "/d", "{url}", "/n", "/q"],
    "neat": ["{exe}", "{url}"],
}

MANAGER_LABELS = {
    "fdm": "🚀 FDM",
    "idm": "⚡ IDM",
    "neat": "💧 Neat DM",
    "direct": "📥 Copy Link",
}

# Hardcoded fallback paths (used only if registry + where.exe miss)
USERNAME = os.getenv("USERNAME", os.getenv("USER", ""))
_FALLBACK_PATHS = {
    "fdm": [
        r"C:\Program Files\Softdeluxe\Free Download Manager\fdm.exe",
        r"C:\Program Files\FreeDownloadManager\fdm.exe",
        r"C:\Program Files (x86)\FreeDownloadManager\fdm.exe",
        r"C:\Program Files (x86)\Softdeluxe\Free Download Manager\fdm.exe",
        rf"C:\Users\{USERNAME}\AppData\Local\Programs\FreeDownloadManager\fdm.exe",
    ],
    "idm": [
        r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe",
        r"C:\Program Files\Internet Download Manager\IDMan.exe",
    ],
    "neat": [
        rf"C:\Users\{USERNAME}\AppData\Local\Neat Download Manager\NeatDM.exe",
        r"C:\Program Files\Neat Download Manager\NeatDM.exe",
        r"C:\Program Files (x86)\Neat Download Manager\NeatDM.exe",
    ],
}

# Registry hives + uninstall key paths to scan
_REG_UNINSTALL_KEYS = [
    (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",),
    (r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",),
]


def _registry_find(exe_name: str) -> str | None:
    """Search Windows registry uninstall entries for an exe. Returns full path or None."""
    try:
        import winreg
    except ImportError:
        return None  # Not on Windows

    hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
    for hive in hives:
        for (key_path,) in _REG_UNINSTALL_KEYS:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    count = winreg.QueryInfoKey(key)[0]
                    for i in range(count):
                        try:
                            sub = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, sub) as sk:
                                for value_name in ("InstallLocation", "InstallDir"):
                                    try:
                                        loc = winreg.QueryValueEx(sk, value_name)[
                                            0
                                        ].strip()
                                        if loc:
                                            candidate = os.path.join(loc, exe_name)
                                            if os.path.isfile(candidate):
                                                return candidate
                                    except FileNotFoundError:
                                        pass
                        except Exception:
                            pass
            except Exception:
                pass
    return None


def _where_find(exe_name: str) -> str | None:
    """Use where.exe to locate an executable on PATH. Returns full path or None."""
    try:
        result = subprocess.run(
            ["where", exe_name],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode == 0:
            first_line = result.stdout.strip().splitlines()[0].strip()
            if os.path.isfile(first_line):
                return first_line
    except Exception:
        pass
    return None


def detect_managers() -> dict[str, str]:
    """
    Dynamically find all supported download managers.
    Search order per manager:
      1. Windows Registry (InstallLocation / InstallDir)
      2. where.exe  (anything on PATH)
      3. Hardcoded fallback paths
    Priority order in returned dict: fdm -> idm -> neat
    """
    found: dict[str, str] = {}

    for mgr_id in ("fdm", "idm", "neat"):  # priority order
        exe_name = MANAGER_EXE_NAMES[mgr_id]

        # 1. Registry
        path = _registry_find(exe_name)
        if path:
            found[mgr_id] = path
            logger.info(f"[OK] Found {mgr_id.upper()} via registry: {path}")
            continue

        # 2. where.exe (PATH)
        path = _where_find(exe_name)
        if path:
            found[mgr_id] = path
            logger.info(f"[OK] Found {mgr_id.upper()} via PATH: {path}")
            continue

        # 3. Hardcoded fallback
        for fb in _FALLBACK_PATHS.get(mgr_id, []):
            if os.path.isfile(fb):
                found[mgr_id] = fb
                logger.info(f"[OK] Found {mgr_id.upper()} via fallback: {fb}")
                break

    if not found:
        logger.warning(
            "[!!] No download managers detected. Links will be copy-paste only."
        )
    return found


INSTALLED_MANAGERS: dict[str, str] = {}  # populated in main()

# Exe names as they appear in Windows tasklist for each manager
MANAGER_PROCESS_NAMES = {
    "fdm": "fdm.exe",
    "idm": "IDMan.exe",
    "neat": "NeatDM.exe",
}


def is_manager_running(manager_id: str) -> bool:
    """Returns True if the manager's process is currently running."""
    proc_name = MANAGER_PROCESS_NAMES.get(manager_id, "")
    if not proc_name:
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {proc_name}", "/NH"],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return proc_name.lower() in result.stdout.lower()
    except Exception:
        return False


async def ensure_manager_running(manager_id: str) -> bool:
    """
    If the manager is installed but not running, launch it and wait up to 5 s
    for it to appear in the process list. Returns True when ready.
    """
    exe = INSTALLED_MANAGERS.get(manager_id)
    if not exe:
        return False

    if is_manager_running(manager_id):
        return True  # already up, nothing to do

    logger.info(
        f"[{manager_id.upper()}] Not running - launching {os.path.basename(exe)}..."
    )
    try:
        # Open the app without passing a URL yet
        subprocess.Popen(
            [exe],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except Exception as e:
        logger.error(f"[{manager_id.upper()}] Failed to launch: {e}")
        return False

    # Poll until the process appears (max 5 s)
    for _ in range(10):
        await asyncio.sleep(0.5)
        if is_manager_running(manager_id):
            logger.info(f"[{manager_id.upper()}] Ready.")
            await asyncio.sleep(0.5)  # small extra buffer for UI init
            return True

    logger.warning(
        f"[{manager_id.upper()}] Launched but did not appear in process list within 5s."
    )
    return False


async def trigger_manager(manager_id: str, url: str) -> bool:
    """Ensures the manager is running, then sends the URL. Returns True on success."""
    exe = INSTALLED_MANAGERS.get(manager_id)
    if not exe:
        return False

    # Auto-launch if installed but closed (FDM priority case)
    ready = await ensure_manager_running(manager_id)
    if not ready:
        logger.warning(
            f"[{manager_id.upper()}] Could not confirm manager is running - attempting anyway."
        )

    cmd_template = MANAGER_COMMANDS.get(manager_id, [])
    cmd = [part.format(exe=exe, url=url) for part in cmd_template]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        await proc.communicate()
        logger.info(f"[{manager_id.upper()}] Triggered download: {url}")
        return True
    except Exception as e:
        logger.error(f"[{manager_id.upper()}] Failed to trigger: {e}")
        return False


async def auto_send(url: str) -> tuple[str, bool]:
    """Try installed managers in priority order: fdm → idm → neat. Returns (manager_id, success)."""
    for mgr in ("fdm", "idm", "neat"):
        if mgr in INSTALLED_MANAGERS:
            ok = await trigger_manager(mgr, url)
            if ok:
                return mgr, True
    return "none", False


# ────────────────────────────────────────────────────────
#  Telethon Client
# ────────────────────────────────────────────────────────
os.makedirs(os.path.join(os.path.dirname(SCRIPT_DIR), "Logs"), exist_ok=True)
client = TelegramClient(
    os.path.join(os.path.dirname(SCRIPT_DIR), "Logs", "fdm_proxy_bot_session"),
    API_ID,
    API_HASH,
    connection_retries=10,  # auto-reconnect on TCP drop
    retry_delay=1,
)

# ────────────────────────────────────────────────────────
#  OpenVPN GUI Core Functions
# ────────────────────────────────────────────────────────
_vpn_connecting_lock = threading.Lock()
_vpn_cancel_connection = False

def connect_vpn():
    """Connect to the VPN using OpenVPN GUI."""
    if not OPENVPN_CONFIG_NAME:
        logger.warning("[VPN] Cannot connect: OpenVPN Config Name is empty.")
        add_event("VPN", "Cannot connect: OpenVPN Config Name is empty.", "warning")
        return False

    if not os.path.isfile(OPENVPN_GUI_PATH):
        logger.warning(f"[VPN] OpenVPN GUI executable not found at: {OPENVPN_GUI_PATH}")
        add_event("VPN", f"OpenVPN GUI executable not found at: {OPENVPN_GUI_PATH}", "error")
        return False

    logger.info(f"[VPN] Connecting to profile '{OPENVPN_CONFIG_NAME}'...")
    add_event("VPN", f"Connecting to profile '{OPENVPN_CONFIG_NAME}'...")
    try:
        subprocess.Popen(
            [OPENVPN_GUI_PATH, "--command", "connect", OPENVPN_CONFIG_NAME],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return True
    except Exception as e:
        logger.error(f"[VPN] Failed to connect: {e}")
        add_event("VPN", f"Failed to connect: {e}", "error")
        return False


def disconnect_vpn():
    """Disconnect the VPN using OpenVPN GUI."""
    if not os.path.isfile(OPENVPN_GUI_PATH):
        logger.warning(f"[VPN] OpenVPN GUI executable not found at: {OPENVPN_GUI_PATH}")
        add_event("VPN", f"OpenVPN GUI executable not found at: {OPENVPN_GUI_PATH}", "error")
        return False

    logger.info("[VPN] Disconnecting VPN connection...")
    add_event("VPN", "Disconnecting VPN...")
    try:
        subprocess.Popen(
            [OPENVPN_GUI_PATH, "--command", "disconnect_all"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return True
    except Exception as e:
        logger.error(f"[VPN] Failed to disconnect: {e}")
        add_event("VPN", f"Failed to disconnect: {e}", "error")
        return False


def check_vpn_status() -> bool:
    """Check if the OpenVPN virtual adapter has an assigned IPv4 address via ipconfig."""
    try:
        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        if result.returncode == 0:
            content = result.stdout
            sections = re.split(r'\n(?=[^\s])', content)
            for section in sections:
                if not section.strip():
                    continue
                is_vpn = False
                desc_match = re.search(r'Description[^:]*:\s*(.*)', section, re.IGNORECASE)
                if desc_match:
                    desc = desc_match.group(1).lower()
                    if any(k in desc for k in ("tap-windows", "wintun", "openvpn", "tap adapter")):
                        is_vpn = True
                
                name_match = re.search(r'^([^\n:]+):', section)
                if name_match:
                    name = name_match.group(1).lower()
                    if "vpn" in name or "openvpn" in name:
                        is_vpn = True
                
                if is_vpn:
                    if "IPv4 Address" in section or "IP Address" in section:
                        if "Media State" in section and "disconnected" in section.lower():
                            continue
                        return True
    except Exception as e:
        logger.warning(f"[VPN] Error running status check: {e}")
    return False


def find_openvpn_profiles(keyword: str) -> list[str]:
    """Find imported OpenVPN profile names containing a keyword (case-insensitive)."""
    config_dirs = []
    user_profile = os.getenv("USERPROFILE")
    if user_profile:
        config_dirs.append(os.path.join(user_profile, "OpenVPN", "config"))
    if OPENVPN_GUI_PATH:
        openvpn_dir = os.path.dirname(os.path.dirname(OPENVPN_GUI_PATH))
        config_dirs.append(os.path.join(openvpn_dir, "config"))
    config_dirs.append(r"C:\Program Files\OpenVPN\config")

    matched_profiles = []
    for cdir in config_dirs:
        if os.path.isdir(cdir):
            try:
                for fname in os.listdir(cdir):
                    if fname.endswith(".ovpn"):
                        name_without_ext = os.path.splitext(fname)[0]
                        if keyword.lower() in name_without_ext.lower():
                            matched_profiles.append(name_without_ext)
            except Exception:
                pass
    return sorted(list(set(matched_profiles)))


def resolve_profiles_for_type(profile_type: str) -> list[str]:
    """Resolve a profile type (e.g. 'US Free') to local OpenVPN config names."""
    if profile_type == "US Free":
        matches = find_openvpn_profiles("us-free")
        return matches if matches else ["us-free"]
    elif profile_type == "Netherlands Free":
        matches = find_openvpn_profiles("nl-free")
        if not matches:
            matches = find_openvpn_profiles("netherlands-free")
        return matches if matches else ["nl-free"]
    elif profile_type == "Japan Free":
        matches = find_openvpn_profiles("jp-free")
        if not matches:
            matches = find_openvpn_profiles("japan-free")
        return matches if matches else ["jp-free"]
    elif profile_type == "Custom Profile":
        if OPENVPN_CONFIG_NAME:
            return [OPENVPN_CONFIG_NAME]
    return []


def get_fallback_order(start_profile_type: str) -> list[str]:
    default_order = ["US Free", "Netherlands Free", "Japan Free"]
    if start_profile_type not in default_order:
        return [start_profile_type] + default_order
    idx = default_order.index(start_profile_type)
    return default_order[idx:] + default_order[:idx]


def connect_vpn_with_fallback():
    """Connect to the VPN, using fallback logic if connection fails within 15 seconds."""
    global _vpn_cancel_connection, OPENVPN_CONFIG_NAME
    
    with _vpn_connecting_lock:
        _vpn_cancel_connection = False
        
    fallback_chain = get_fallback_order(OPENVPN_PROFILE_TYPE)
    logger.info(f"[VPN] Starting VPN connection fallback chain: {fallback_chain}")
    add_event("VPN", "Starting connection fallback...")
    
    for profile_type in fallback_chain:
        with _vpn_connecting_lock:
            if _vpn_cancel_connection or not VPN_TOGGLE:
                logger.info("[VPN] Connection attempt cancelled by user.")
                add_event("VPN", "Connection cancelled by user.")
                return False
                
        candidates = resolve_profiles_for_type(profile_type)
        if not candidates:
            continue
            
        logger.info(f"[VPN] Trying '{profile_type}' candidates: {candidates}")
        
        for candidate in candidates:
            with _vpn_connecting_lock:
                if _vpn_cancel_connection or not VPN_TOGGLE:
                    logger.info("[VPN] Connection attempt cancelled.")
                    add_event("VPN", "Connection cancelled.")
                    return False
            
            original_config_name = OPENVPN_CONFIG_NAME
            OPENVPN_CONFIG_NAME = candidate
            
            success = connect_vpn()
            OPENVPN_CONFIG_NAME = original_config_name
            
            if not success:
                continue
                
            connected = False
            for _ in range(30):  # 15 seconds
                with _vpn_connecting_lock:
                    if _vpn_cancel_connection or not VPN_TOGGLE:
                        logger.info("[VPN] Connection cancelled by user.")
                        disconnect_vpn()
                        return False
                if check_vpn_status():
                    connected = True
                    break
                time.sleep(0.5)
                
            if connected:
                logger.info(f"[VPN] Connected to '{candidate}'!")
                add_event("VPN", f"Connected to '{candidate}'", "info")
                return True
            else:
                logger.warning(f"[VPN] Connection to '{candidate}' timed out.")
                add_event("VPN", f"Connection to '{candidate}' timed out", "warning")
                disconnect_vpn()
                time.sleep(1.0)
                
    logger.error("[VPN] All VPN profiles in fallback chain failed.")
    add_event("VPN", "All fallback profiles failed.", "error")
    if LogDashboard._instance and LogDashboard._instance.running:
        try:
            LogDashboard._instance.queue.put((LogDashboard._instance._update_vpn_gui_status, (False,)))
        except Exception:
            pass
    return False


def cancel_vpn_connection():
    global _vpn_cancel_connection
    with _vpn_connecting_lock:
        _vpn_cancel_connection = True

# Batch state
batch_active = False
batch_links: list[str] = []

# Option N: speed-stats registry — keyed by (chat_id, message_id)
download_registry: dict[tuple, dict] = {}
active_downloads: set[tuple] = set()

# ────────────────────────────────────────────────────────
#  State Persistence & Network Monitoring
# ────────────────────────────────────────────────────────
STATE_FILE = os.path.join(ROOT_DIR, "Logs", "proxy_state.json")
proxy_state = {
    "last_seen_message_ids": {}
}

def load_proxy_state():
    global proxy_state
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                proxy_state = json.load(f)
            if "last_seen_message_ids" not in proxy_state:
                proxy_state["last_seen_message_ids"] = {}
    except Exception as e:
        logger.error(f"Error loading proxy state: {e}")

def save_proxy_state():
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(proxy_state, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving proxy state: {e}")

def update_last_seen(chat_id: int, message_id: int):
    load_proxy_state()
    last_seen = proxy_state.setdefault("last_seen_message_ids", {})
    curr = last_seen.get(str(chat_id), 0)
    if message_id > curr:
        last_seen[str(chat_id)] = message_id
        save_proxy_state()

async def initialize_channel_state(channel):
    try:
        async for msg in client.iter_messages(channel, limit=1):
            load_proxy_state()
            proxy_state.setdefault("last_seen_message_ids", {})[str(channel)] = msg.id
            save_proxy_state()
            logger.info(f"[STATE] Initialized last_seen for channel {channel} to {msg.id}")
            break
    except Exception as e:
        logger.warning(f"[STATE] Could not initialize last_seen for {channel}: {e}")

async def _network_monitor_loop():
    """Background task to monitor internet connection and trigger recovery upon restoration."""
    logger.info("[NET] Network monitor loop started.")
    is_online = True
    
    while True:
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: socket.create_connection(("8.8.8.8", 53), timeout=3).close()
            )
            ping_success = True
        except Exception:
            ping_success = False

        if ping_success:
            if not is_online:
                logger.info("[NET] Network connection restored! Triggering recovery handler...")
                add_event("SYSTEM", "Network connection restored! Starting recovery...", "info")
                is_online = True
                asyncio.create_task(_run_recovery())
        else:
            if is_online:
                logger.warning("[NET] Network connection lost.")
                add_event("SYSTEM", "Network connection lost.", "warning")
                is_online = False
                
        await asyncio.sleep(15)

async def _run_recovery():
    """Performs the recovery actions: catches up on missed channel messages and retries failed downloads."""
    try:
        for _ in range(10):
            if client.is_connected() and await client.is_user_authorized():
                break
            await asyncio.sleep(1)
        else:
            logger.warning("[RECOVERY] Telegram client not ready. Aborting recovery run.")
            return

        logger.info("[RECOVERY] Starting recovery run...")
        add_event("SYSTEM", "Recovery in progress: scanning for missed messages...")

        load_proxy_state()
        last_seen = proxy_state.setdefault("last_seen_message_ids", {})
        
        for chat_id in list(ACTIVE_CHANNELS):
            last_id = last_seen.get(str(chat_id), 0)
            if not last_id:
                try:
                    async for msg in client.iter_messages(chat_id, limit=1):
                        last_seen[str(chat_id)] = msg.id
                        save_proxy_state()
                except Exception as e:
                    logger.warning(f"[RECOVERY] Could not init last_seen for {chat_id}: {e}")
                continue

            try:
                messages = []
                async for msg in client.iter_messages(chat_id, min_id=last_id, limit=100):
                    messages.append(msg)
                
                messages.reverse()
                
                if messages:
                    logger.info(f"[RECOVERY] Found {len(messages)} missed messages in channel {chat_id}.")
                    add_event("SYSTEM", f"Found {len(messages)} missed messages in watch list.")
                
                for msg in messages:
                    await _sniffer_handler(msg)
                    
            except Exception as e:
                logger.error(f"[RECOVERY] Error catching up on channel {chat_id}: {e}")

        logger.info("[RECOVERY] Scanning for incomplete/failed downloads...")
        add_event("SYSTEM", "Recovery: checking for incomplete/failed downloads...")
        
        triggered_retry_count = 0
        for key, reg in list(download_registry.items()):
            chat_id, message_id = key
            
            size_bytes = reg.get("size_bytes", 0)
            completed_ranges = reg.get("completed_ranges", [])
            
            intervals = sorted(completed_ranges)
            merged = []
            for interval in intervals:
                if not merged or merged[-1][1] < interval[0] - 1:
                    merged.append(list(interval))
                else:
                    merged[-1][1] = max(merged[-1][1], interval[1])
            total_unique_bytes = sum(item[1] - item[0] + 1 for item in merged)
            
            if total_unique_bytes < size_bytes and key not in active_downloads:
                link = f"http://{PROXY_HOST}:{PROXY_PORT}/dl/{chat_id}/{message_id}"
                file_name = reg.get("fname", "Unknown File")
                logger.info(f"[RECOVERY] Re-triggering failed download: {file_name} ({total_unique_bytes}/{size_bytes} bytes done)")
                add_event("DOWNLOAD", f"Re-triggering failed download: {file_name}")
                
                mgr, pushed = await auto_send(link)
                if pushed:
                    triggered_retry_count += 1
                    
        if triggered_retry_count > 0:
            add_event("SYSTEM", f"Recovery finished: re-triggered {triggered_retry_count} failed downloads.")
        else:
            add_event("SYSTEM", "Recovery finished: no failed downloads to retry.")

    except Exception as e:
        logger.error(f"[RECOVERY] Error in recovery handler: {e}")


async def _download_chunk_task(media, offset, limit, chunk_size, max_retries):
    """Download a single chunk of media from Telegram with retries."""
    for attempt in range(max_retries + 1):
        try:
            chunks = []
            async for c in client.iter_download(
                media, offset=offset, limit=limit, chunk_size=chunk_size
            ):
                if c:
                    chunks.append(c)
            return b"".join(chunks)
        except Exception as e:
            if attempt == max_retries:
                logger.error(
                    f"[DOWNLOAD] Chunk at offset {offset} failed after {max_retries} retries: {e}"
                )
                raise e
            logger.warning(
                "[DOWNLOAD] Chunk at offset %s failed (attempt %s/%s): %s. Retrying...",
                offset,
                attempt + 1,
                max_retries + 1,
                e,
            )
            await asyncio.sleep(0.5 * (attempt + 1))


# ────────────────────────────────────────────────────────
#  HTTP Proxy Handler (serves file chunks to the DM)
# ────────────────────────────────────────────────────────
async def handle_download(request: web.Request) -> web.StreamResponse:
    chat_id = int(request.match_info["chat_id"])
    message_id = int(request.match_info["message_id"])
    response = None
    _bytes_written = 0
    _key = (chat_id, message_id)
    active_downloads.add(_key)

    if _key not in download_registry:
        download_registry[_key] = {
            "start": time.monotonic(),
            "reply_chat": None,
            "reply_to": None,
            "fname": f"tg_media_{message_id}.bin",
            "size_bytes": 0,
            "notified": False,
            "opened": False,
            "completed_ranges": [],
        }

    try:
        # Retrieve the specific message containing the media (from tg_fdm_proxy 1.py)
        message = await client.get_messages(chat_id, ids=message_id)
        if not message or not message.media or not hasattr(message, "file"):
            add_event(
                "ERROR", f"File not found: chat {chat_id}, msg {message_id}", "error"
            )
            return web.Response(
                status=404, text="Message not found or does not contain media."
            )

        file_size = int(message.file.size)  # ensure int — Telegram can return float
        raw_name = (
            message.file.name if message.file.name else f"tg_media_{message_id}.bin"
        )
        raw_name = "".join(
            [c for c in raw_name if (c.isalnum() or c in " .-_()")]
        ).strip()
        # Option S: rename to clean format
        file_name = auto_rename(raw_name)

        if _key in download_registry:
            download_registry[_key]["fname"] = file_name
            download_registry[_key]["size_bytes"] = file_size

        range_header = request.headers.get("Range", "")
        status = 200
        start = 0
        end = file_size - 1

        # Parse HTTP Range Header for multi-threaded downloading in FDM
        if range_header:
            match = re.search(r"bytes=(\d+)-(\d*)", range_header)
            if match:
                start = int(match.group(1))
                if match.group(2):
                    end = int(match.group(2))
                else:
                    end = file_size - 1
            # Keep start and end within file boundary
            if start >= file_size:
                return web.Response(
                    status=416,
                    text="Requested Range Not Satisfiable",
                    headers={"Content-Range": f"bytes */{file_size}"},
                )
            end = min(end, file_size - 1)
            status = 206

        length = int(end - start + 1)  # must be int for iter_download

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Content-Length": str(length),
        }

        response = web.StreamResponse(status=status, headers=headers)
        await response.prepare(request)

        # Ultra-minimal real download loop with offset alignment
        chunk_size = 1024 * 1024  # 1 MB aligned chunk size required by Telethon
        aligned_offset = (start // chunk_size) * chunk_size
        bytes_to_skip = start - aligned_offset

        # Download logic based on method
        if DOWNLOAD_METHOD == "parallel":
            # Parallel chunk downloader
            max_concurrency = int(os.getenv("MAX_PARALLEL_CHUNKS", "8").strip())
            max_retries = int(os.getenv("MAX_RETRIES", "3").strip())

            chunk_ranges = []
            curr_offset = aligned_offset
            while curr_offset < aligned_offset + length + bytes_to_skip:
                curr_limit = min(
                    chunk_size, aligned_offset + length + bytes_to_skip - curr_offset
                )
                chunk_ranges.append((curr_offset, curr_limit))
                curr_offset += curr_limit

            total_chunks = len(chunk_ranges)
            active_tasks = {}

            # Pre-schedule first batch
            for idx in range(min(max_concurrency - 1, total_chunks)):
                off, lim = chunk_ranges[idx]
                active_tasks[idx] = asyncio.create_task(
                    _download_chunk_task(
                        message.media, off, lim, chunk_size, max_retries
                    )
                )

            try:
                for idx in range(total_chunks):
                    # Schedule next chunk ahead to maintain sliding window
                    next_to_schedule = idx + max_concurrency - 1
                    if (
                        next_to_schedule < total_chunks
                        and next_to_schedule not in active_tasks
                    ):
                        off, lim = chunk_ranges[next_to_schedule]
                        active_tasks[next_to_schedule] = asyncio.create_task(
                            _download_chunk_task(
                                message.media, off, lim, chunk_size, max_retries
                            )
                        )

                    task = active_tasks.get(idx)
                    if not task:
                        off, lim = chunk_ranges[idx]
                        task = asyncio.create_task(
                            _download_chunk_task(
                                message.media, off, lim, chunk_size, max_retries
                            )
                        )
                        active_tasks[idx] = task

                    chunk_data = await task

                    if bytes_to_skip > 0:
                        chunk_data = chunk_data[bytes_to_skip:]
                        bytes_to_skip = 0

                    if _bytes_written + len(chunk_data) > length:
                        chunk_data = chunk_data[: length - _bytes_written]

                    if not chunk_data:
                        break

                    await response.write(chunk_data)
                    _bytes_written += len(chunk_data)

                    del active_tasks[idx]

                    if _bytes_written >= length:
                        break
            except Exception as e:
                # Cancel any remaining tasks
                for t in active_tasks.values():
                    if not t.done():
                        t.cancel()
                raise e
        else:
            # Sequential chunk downloader (original logic)
            try:
                async for chunk in client.iter_download(
                    message.media,
                    offset=aligned_offset,
                    limit=length + bytes_to_skip,
                    chunk_size=chunk_size,
                ):
                    if not chunk:
                        break

                    if bytes_to_skip > 0:
                        # Discard the overlapping bytes from the aligned boundary
                        chunk = chunk[bytes_to_skip:]
                        bytes_to_skip = 0

                    # Prevent sending more bytes than the HTTP client requested
                    if _bytes_written + len(chunk) > length:
                        chunk = chunk[: length - _bytes_written]

                    if not chunk:
                        break

                    await response.write(chunk)
                    _bytes_written += len(chunk)

                    if _bytes_written >= length:
                        break
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass  # Harmless client disconnect

        # Track completed ranges and check for full completion
        if _bytes_written == length:
            if _key in download_registry:
                reg = download_registry[_key]
                if "completed_ranges" not in reg:
                    reg["completed_ranges"] = []
                reg["completed_ranges"].append((start, end))

                # Merge overlapping intervals to calculate total unique bytes completed
                intervals = sorted(reg["completed_ranges"])
                merged = []
                for interval in intervals:
                    if not merged or merged[-1][1] < interval[0] - 1:
                        merged.append(list(interval))
                    else:
                        merged[-1][1] = max(merged[-1][1], interval[1])
                total_unique_bytes = sum(item[1] - item[0] + 1 for item in merged)

                # Check if fully complete
                if total_unique_bytes >= reg["size_bytes"]:
                    # 1. Open Download Folder (exactly once)
                    if not reg.get("opened", False):
                        reg["opened"] = True
                        logger.info(
                            f"[DOWNLOAD] Opening download folder automatically for {file_name}"
                        )
                        add_event(
                            "DOWNLOAD", f"Opening download folder for {file_name}"
                        )
                        try:
                            if os.path.exists(DOWNLOAD_DIR):
                                os.startfile(DOWNLOAD_DIR)
                        except Exception as err:
                            logger.error(
                                f"[DOWNLOAD] Failed to open download folder: {err}"
                            )

                    # 2. Dispatch speed-stats Telegram reply (exactly once)
                    if not reg.get("notified", False):
                        reg["notified"] = True
                        _elapsed = time.monotonic() - reg["start"]
                        _speed_mb = (
                            reg["size_bytes"] / max(_elapsed, 0.1) / (1024 * 1024)
                        )
                        _size_gb = reg["size_bytes"] / (1024**3)
                        _mins, _secs = divmod(int(_elapsed), 60)
                        _time_str = f"{_mins}m {_secs}s" if _mins else f"{_secs}s"

                        # Log finished stats
                        add_event(
                            "DOWNLOAD",
                            f"Finished {file_name} — {_size_gb:.2f} GB in {_time_str} (~{_speed_mb:.1f} MB/s)",
                        )

                        if reg.get("reply_chat"):

                            async def _send_stats(
                                _i=reg, _ts=_time_str, _sm=_speed_mb, _sg=_size_gb
                            ):
                                try:
                                    await client.send_message(
                                        _i["reply_chat"],
                                        f"📊 `{_i['fname']}` — {_sg:.2f} GB in {_ts} (~{_sm:.1f} MB/s)",
                                        reply_to=_i["reply_to"],
                                    )
                                except Exception as _stat_err:
                                    logger.warning(
                                        f"[STATS] Could not send speed stats: {_stat_err}"
                                    )

                            asyncio.create_task(_send_stats())

        return response

    except ConnectionResetError:
        # FDM closed a specific connection thread — standard behaviour in multi-threading
        return response
    except Exception as e:
        print(f"Error during download for chat {chat_id}, message {message_id}: {e}")
        logger.error(f"Download error for chat {chat_id}, message {message_id}: {e}")
        add_event(
            "ERROR", f"Download failed for {chat_id}/{message_id}: {str(e)}", "error"
        )
        return web.Response(status=500, text=f"Download failed: {str(e)}")
    finally:
        active_downloads.discard(_key)


# ────────────────────────────────────────────────────────
#  Helper: Build smart button row based on installed DMs
# ────────────────────────────────────────────────────────
def make_buttons(chat_id: int, message_id: int) -> list:
    """Build inline buttons — only show buttons for installed managers + direct link."""
    row1, row2 = [], []

    for mgr in ("fdm", "idm", "neat"):
        if mgr in INSTALLED_MANAGERS:
            row1.append(
                Button.inline(
                    MANAGER_LABELS[mgr], data=f"dl_{mgr}_{chat_id}_{message_id}"
                )
            )

    row2.append(
        Button.inline(
            MANAGER_LABELS["direct"], data=f"dl_direct_{chat_id}_{message_id}"
        )
    )

    buttons = []
    if row1:
        buttons.append(row1)
    buttons.append(row2)
    return buttons


# ────────────────────────────────────────────────────────
#  Batch Commands
# ────────────────────────────────────────────────────────
@client.on(events.NewMessage(incoming=True, pattern="/start_batch"))
async def start_batch(event):
    global batch_active, batch_links
    batch_active = True
    batch_links = []
    await event.reply(
        "📦 **Batch Mode Active**\n"
        "Forward files to add them to the queue.\n\n"
        "▸ Use `/end_batch` to finalize and push to your download manager."
    )


@client.on(events.NewMessage(incoming=True, pattern="/end_batch"))
async def end_batch(event):
    global batch_active, batch_links
    if not batch_active:
        await event.reply("⚠️ **No Active Batch** — use `/start_batch` first.")
        return
    if not batch_links:
        await event.reply("📂 **Batch is Empty** — forward some files first.")
        batch_active = False
        return

    success_count = 0
    if INSTALLED_MANAGERS:
        await event.reply(f"🚀 Pushing {len(batch_links)} files to download manager...")
        for link in batch_links:
            _, ok = await auto_send(link)
            if ok:
                success_count += 1
            await asyncio.sleep(0.5)

    txt_stream = io.BytesIO("\n".join(batch_links).encode("utf-8"))
    txt_stream.name = "fdm_batch_links.txt"

    if success_count > 0:
        reply = (
            f"✅ **Batch Complete** — {success_count}/{len(batch_links)} pushed.\n"
            f"_(Backup link list attached)_"
        )
    else:
        reply = "📥 **No manager found.** Import the attached .txt into your download manager:"

    await event.reply(reply, file=txt_stream)
    batch_active = False
    batch_links = []


@client.on(events.NewMessage(incoming=True, pattern=r"^/(?:commands|help|start)$"))
async def show_commands(event):
    """Show the list of all available commands."""
    await event.reply(
        "🤖 **Telegram FDM Proxy Bot Commands:**\n\n"
        "📦 **Batch Downloads:**\n"
        "• `/start_batch` — Start collecting files in a batch queue\n"
        "• `/end_batch` — Stop collecting and push all files to FDM\n\n"
        "📡 **Channel Watcher:**\n"
        "• `/channel` — Manage watched channels watchlist via GUI\n"
        "• `/channels` — List all currently watched channels\n"
        "• `/add_channel <username/ID>` — Add a channel to the watch list\n"
        "• `/remove_channel <username/ID>` — Remove a channel from the watch list\n\n"
        "❓ **General:**\n"
        "• `/commands` or `/help` — Show this list of available commands"
    )


# ────────────────────────────────────────────────────────
#  Channel Auto-Sniffer
# ────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────
#  Dynamic Channel Management  (/channels, /add_channel, /remove_channel)
# ────────────────────────────────────────────────────────
# Pre-loaded from .env TARGET_CHANNELS; editable at runtime via commands
ACTIVE_CHANNELS: set = set(TARGET_CHANNELS)


@client.on(events.NewMessage(incoming=True, pattern=r"/channel$"))
async def cmd_channel_select_gui(event):
    """Open channel select GUI for watchlist."""
    buttons = ReplyKeyboardMarkup(
        rows=[
            KeyboardButtonRow(
                buttons=[
                    KeyboardButtonRequestPeer(
                        text="📡 Watch Channel (Add)",
                        button_id=1,
                        peer_type=RequestPeerTypeBroadcast(),
                        max_quantity=1,
                    ),
                    KeyboardButtonRequestPeer(
                        text="🗑️ Stop Watching (Remove)",
                        button_id=2,
                        peer_type=RequestPeerTypeBroadcast(),
                        max_quantity=1,
                    ),
                ]
            )
        ],
        resize=True,
        single_use=True,
    )
    await event.reply("Choose an action to manage your watchlist:", buttons=buttons)


@client.on(events.NewMessage(incoming=True, pattern="/channels"))
async def cmd_channels(event):
    """List all currently watched channels."""
    if not ACTIVE_CHANNELS:
        await event.reply(
            "📡 **No channels being watched.**\n\n"
            "Add one with:\n`/add_channel @username` or `/add_channel -1001234567890`"
        )
        return
    lines = "\n".join(f"  • `{ch}`" for ch in sorted(str(c) for c in ACTIVE_CHANNELS))
    await event.reply(
        f"📡 **Watched Channels ({len(ACTIVE_CHANNELS)}):**\n{lines}\n\n"
        f"▸ `/add_channel <id>` — start watching a channel\n"
        f"▸ `/remove_channel <id>` — stop watching a channel"
    )


@client.on(events.NewMessage(incoming=True, pattern=r"/add_channel(?: (.+))?"))
async def cmd_add_channel(event):
    """Add a channel to the auto-sniffer. Usage: /add_channel @username or -100id"""
    arg = event.pattern_match.group(1)
    if not arg:
        buttons = ReplyKeyboardMarkup(
            rows=[
                KeyboardButtonRow(
                    buttons=[
                        KeyboardButtonRequestPeer(
                            text="📡 Select Channel to Watch",
                            button_id=1,
                            peer_type=RequestPeerTypeBroadcast(),
                            max_quantity=1,
                        )
                    ]
                )
            ],
            resize=True,
            single_use=True,
        )
        await event.reply(
            "Tap the button below to choose a channel to watch, or type `/add_channel <username/ID>`:",
            buttons=buttons,
        )
        return
    arg = arg.strip()
    channel = int(arg) if arg.lstrip("-").isdigit() else arg
    if channel in ACTIVE_CHANNELS:
        await event.reply(f"✅ `{channel}` is already being watched.")
        return
    ACTIVE_CHANNELS.add(channel)
    await initialize_channel_state(channel)
    save_config_to_env(
        {"TARGET_CHANNELS": ",".join(str(ch) for ch in sorted(ACTIVE_CHANNELS))}
    )
    logger.info(f"[CHANNELS] Added: {channel}  |  Active: {ACTIVE_CHANNELS}")
    await event.reply(
        f"✅ Now watching `{channel}`.\nTotal: **{len(ACTIVE_CHANNELS)}** channel(s)."
    )


@client.on(events.NewMessage(incoming=True, pattern=r"/remove_channel(?: (.+))?"))
async def cmd_remove_channel(event):
    """Remove a channel from the auto-sniffer."""
    arg = event.pattern_match.group(1)
    if not arg:
        buttons = ReplyKeyboardMarkup(
            rows=[
                KeyboardButtonRow(
                    buttons=[
                        KeyboardButtonRequestPeer(
                            text="🗑️ Select Channel to Stop Watching",
                            button_id=2,
                            peer_type=RequestPeerTypeBroadcast(),
                            max_quantity=1,
                        )
                    ]
                )
            ],
            resize=True,
            single_use=True,
        )
        await event.reply(
            "Tap the button below to choose a channel to stop watching, or type `/remove_channel <username/ID>`:",
            buttons=buttons,
        )
        return
    arg = arg.strip()
    channel = int(arg) if arg.lstrip("-").isdigit() else arg
    if channel not in ACTIVE_CHANNELS:
        await event.reply(f"⚠️ `{channel}` is not in the watch list.")
        return
    ACTIVE_CHANNELS.discard(channel)
    save_config_to_env(
        {"TARGET_CHANNELS": ",".join(str(ch) for ch in sorted(ACTIVE_CHANNELS))}
    )
    logger.info(f"[CHANNELS] Removed: {channel}  |  Active: {ACTIVE_CHANNELS}")
    await event.reply(
        f"🗑️ Removed `{channel}`.\nRemaining: **{len(ACTIVE_CHANNELS)}** channel(s)."
    )


# ────────────────────────────────────────────────────────
#  Quality-Selection Engine
#  Groups quality variants (1080p / 720p / SD) of the same file and picks best
# ────────────────────────────────────────────────────────

# Resolution priority (higher = better)
_RES_RANK = [
    ("2160p", 2160),
    ("4k", 2160),
    ("uhd", 2160),
    ("1080p", 1080),
    ("1080i", 1080),
    ("720p", 720),
    ("720i", 720),
    ("480p", 480),
    ("360p", 360),
    ("240p", 240),
]

# Buffers: key = (chat_id, group_key)
_quality_buffer: dict[tuple, list[dict]] = {}
_quality_timers: dict[tuple, asyncio.Task] = {}


def _quality_score(fname: str, size: int) -> tuple[int, int]:
    """Return (resolution_rank, size_bytes) — higher is better."""
    name = fname.lower()
    for keyword, rank in _RES_RANK:
        if keyword in name:
            return rank, size
    return 0, size  # no resolution tag — fall back to largest size


def _group_key(fname: str, media_group_id) -> str:
    """
    Unique key for a 'batch' of quality variants.
    - Same Telegram album  → use album id (exact)
    - Sequential messages  → strip quality/size tokens from filename and normalise
    """
    if media_group_id:
        return f"album_{media_group_id}"
    # Strip common quality/codec/size tokens to find the movie title core
    base = fname.lower()
    base = re.sub(
        r"[\._\-\s]*("
        r"2160p?|4k|uhd|1080p?|720p?|480p?|360p?|240p?"
        r"|x264|x265|hevc|avc|hdrip|bluray|bdrip|webrip|web-dl|web|hq"
        r"|esub|aac|dd\d|dts|atmos|ac3|eac3"
        r"|multi|dual|hindi|tamil|telugu|english|dubbed"
        r"|\d{2,4}mb"
        r")",
        "",
        base,
        flags=re.IGNORECASE,
    )
    base = re.sub(r"[^a-z0-9]", "", base)[
        :35
    ]  # keep alphanumeric only, cap at 35 chars
    return f"name_{base}" if base else "name_unknown"


async def _flush_quality_group(buf_key: tuple) -> None:
    """
    Called after QUALITY_WAIT_SECS timeout.
    Picks the best candidate and triggers the download.
    """
    candidates = _quality_buffer.pop(buf_key, [])
    _quality_timers.pop(buf_key, None)

    if not candidates:
        return

    # Sort: highest resolution first, then largest size
    best = max(candidates, key=lambda c: _quality_score(c["fname"], c["size"]))
    res_rank, _ = _quality_score(best["fname"], best["size"])
    res_label = f"{res_rank}p" if res_rank else "best size"

    chat_id = best["chat_id"]
    message_id = best["message_id"]
    link = f"http://{PROXY_HOST}:{PROXY_PORT}/dl/{chat_id}/{message_id}"
    fname = best["fname"]
    size_mb = best["size"] / (1024 * 1024)
    event = best["event"]

    # Option P: keyword filter
    fname_lower = fname.lower()
    if KEYWORD_BLOCK and any(kw in fname_lower for kw in KEYWORD_BLOCK):
        logger.info(f"[FILTER-P] Blocked '{fname}' — keyword match")
        return
    if KEYWORD_ALLOW and not any(kw in fname_lower for kw in KEYWORD_ALLOW):
        logger.info(f"[FILTER-P] Skipped '{fname}' — no KEYWORD_ALLOW match")
        return

    # Option O: duplicate guard
    if _is_duplicate(chat_id, message_id):
        logger.info(f"[DEDUP] Already triggered ({chat_id}/{message_id}), skipping.")
        return

    skipped = len(candidates) - 1
    logger.info(
        f"[QUALITY] Winner: '{fname}' ({res_label}, {size_mb:.0f} MB) "
        f"from {skipped + 1} variant(s)"
    )
    add_event("QUALITY", f"Winner: {fname} ({res_label}, {size_mb:.0f} MB)")

    mgr, pushed = await auto_send(link)
    label = MANAGER_LABELS.get(mgr, mgr)

    skip_note = f"\n└ _{skipped} lower-quality variant(s) skipped_" if skipped else ""
    if pushed:
        _sent = await event.reply(
            f"🏆 **Best Quality → {label}**\n"
            f"└ `{fname}`\n"
            f"└ {res_label} · {size_mb:.0f} MB"
            f"{skip_note}"
        )
        download_registry[(chat_id, message_id)] = {
            "start": time.monotonic(),
            "reply_chat": _sent.chat_id,
            "reply_to": _sent.id,
            "fname": fname,
            "size_bytes": best["size"],
            "notified": False,
        }
    else:
        await event.reply(
            f"📄 **Best Quality Ready**\n"
            f"└ `{fname}` · {res_label} · {size_mb:.0f} MB{skip_note}\n"
            f"`{link}`"
        )


# ────────────────────────────────────────────────────────
#  Channel Auto-Sniffer  (checks live ACTIVE_CHANNELS set)
# ────────────────────────────────────────────────────────
async def _sniffer_handler(event):
    """Handles new file messages in watched channels with quality-selection buffering."""
    if event.chat_id not in ACTIVE_CHANNELS:
        return
    if not (event.message.media and event.message.file):
        return
    update_last_seen(event.chat_id, event.id)

    fname = event.message.file.name or "Unknown File"
    size = event.message.file.size
    size_mb = size / (1024 * 1024)

    if size_mb < MIN_FILE_SIZE_MB:
        return

    # Option G: extension whitelist
    if ALLOWED_EXT:
        _ext = os.path.splitext(fname)[1].lower()
        if _ext not in ALLOWED_EXT:
            logger.info(f"[FILTER] Skipped '{fname}' — '{_ext}' not in ALLOWED_EXT")
            add_event(
                "BUFFER", f"Skipped '{fname}' (ext '{_ext}' not allowed)", "warning"
            )
            return

    # Quality-selection: buffer this candidate
    gkey = _group_key(fname, getattr(event.message, "grouped_id", None))
    buf_key = (event.chat_id, gkey)

    _quality_buffer.setdefault(buf_key, []).append(
        {
            "chat_id": event.chat_id,
            "message_id": event.id,
            "fname": fname,
            "size": size,
            "event": event,
        }
    )

    # Cancel existing timer and restart the wait window
    existing = _quality_timers.get(buf_key)
    if existing and not existing.done():
        existing.cancel()

    res_rank, _ = _quality_score(fname, size)
    res_label = f"{res_rank}p" if res_rank else f"{size_mb:.0f} MB"
    logger.info(
        f"[QUALITY] Buffered: '{fname}' ({res_label}) — waiting {QUALITY_WAIT_SECS}s for more variants"
    )
    add_event("BUFFER", f"Buffered variant: {fname} ({res_label})")

    _quality_timers[buf_key] = asyncio.ensure_future(_delayed_flush(buf_key))


async def _delayed_flush(buf_key: tuple) -> None:
    """Sleep then flush the quality group."""
    await asyncio.sleep(QUALITY_WAIT_SECS)
    await _flush_quality_group(buf_key)


client.add_event_handler(
    _sniffer_handler,
    events.NewMessage(),
)


# ────────────────────────────────────────────────────────
#  Main Message Handler
# ────────────────────────────────────────────────────────
@client.on(events.NewMessage(incoming=True))
async def on_new_message(event):

    # Intercept requested peer updates (Option C)
    if event.message.action and isinstance(
        event.message.action, MessageActionRequestedPeerSentMe
    ):
        action = event.message.action
        if action.button_id in (1, 2):
            peers = action.peers
            if peers:
                peer = peers[0]
                if isinstance(peer, RequestedPeerChannel):
                    try:
                        entity = await client.get_entity(PeerChannel(peer.channel_id))
                        signed_id = utils.get_peer_id(entity)
                        title = entity.title

                        if action.button_id == 1:
                            if signed_id in ACTIVE_CHANNELS:
                                await event.reply(
                                    f"✅ `{title}` (ID: `{signed_id}`) is already being watched.",
                                    buttons=Button.clear(),
                                )
                                return
                            ACTIVE_CHANNELS.add(signed_id)
                            await initialize_channel_state(signed_id)
                            save_config_to_env(
                                {
                                    "TARGET_CHANNELS": ",".join(
                                        str(ch) for ch in sorted(ACTIVE_CHANNELS)
                                    )
                                }
                            )
                            logger.info(
                                f"[CHANNELS] Added via GUI: {title} ({signed_id})"
                            )
                            await event.reply(
                                f"✅ **Added Watch Channel**\n"
                                f"• **Title**: `{title}`\n"
                                f"• **ID**: `{signed_id}`\n\n"
                                f"Total: **{len(ACTIVE_CHANNELS)}** channel(s).",
                                buttons=Button.clear(),
                            )
                        elif action.button_id == 2:
                            if signed_id not in ACTIVE_CHANNELS:
                                await event.reply(
                                    f"⚠️ `{title}` (ID: `{signed_id}`) is not in the watch list.",
                                    buttons=Button.clear(),
                                )
                                return
                            ACTIVE_CHANNELS.discard(signed_id)
                            save_config_to_env(
                                {
                                    "TARGET_CHANNELS": ",".join(
                                        str(ch) for ch in sorted(ACTIVE_CHANNELS)
                                    )
                                }
                            )
                            logger.info(
                                f"[CHANNELS] Removed via GUI: {title} ({signed_id})"
                            )
                            await event.reply(
                                f"🗑️ **Removed Watch Channel**\n"
                                f"• **Title**: `{title}`\n"
                                f"• **ID**: `{signed_id}`\n\n"
                                f"Total: **{len(ACTIVE_CHANNELS)}** channel(s).",
                                buttons=Button.clear(),
                            )
                    except Exception as ex:
                        logger.error(f"Error handling peer select action: {ex}")
                        await event.reply(
                            f"❌ Failed to resolve selection: {ex}",
                            buttons=Button.clear(),
                        )
                else:
                    await event.reply(
                        "⚠️ Please select a channel (broadcast), not a user or group.",
                        buttons=Button.clear(),
                    )
            return

    if event.message.text and event.message.text.startswith("/"):
        return
    if not (event.message.media and event.message.file):
        return

    chat_id = event.chat_id
    message_id = event.id
    update_last_seen(chat_id, message_id)
    link = f"http://{PROXY_HOST}:{PROXY_PORT}/dl/{chat_id}/{message_id}"
    fname = event.message.file.name or "Unknown File"
    size_mb = event.message.file.size / (1024 * 1024)

    if batch_active:
        batch_links.append(link)
        logger.info(f"Queued: {fname}")
        await event.reply(
            f"📥 **Added to Batch Queue**\n"
            f"└ `{fname}` ({size_mb:.2f} MB)\n"
            f"📊 Total: {len(batch_links)}",
            buttons=[
                [Button.inline("Copy Link", data=f"dl_direct_{chat_id}_{message_id}")]
            ],
        )
        return

    logger.info(
        f"Received: {fname} ({size_mb:.2f} MB) — chat {chat_id}, msg {message_id}"
    )
    add_event("RECEIVE", f"{fname} ({size_mb:.2f} MB)")

    # Option O: duplicate guard
    if _is_duplicate(chat_id, message_id):
        add_event("RECEIVE", f"Ignored duplicate file: {fname}", "warning")
        return

    # Auto-trigger installed download manager immediately
    mgr, pushed = await auto_send(link)
    buttons = make_buttons(chat_id, message_id)

    if pushed:
        add_event("DOWNLOAD", f"Pushed to {mgr.upper()}: {fname}")
        _sent = await event.reply(
            f"✅ **Sent to {MANAGER_LABELS.get(mgr, mgr)}**\n"
            f"└ `{fname}` ({size_mb:.2f} MB)",
            buttons=buttons,
        )
        # Option N: register for speed-stats reply
        download_registry[(chat_id, message_id)] = {
            "start": time.monotonic(),
            "reply_chat": _sent.chat_id,
            "reply_to": _sent.id,
            "fname": fname,
            "size_bytes": event.message.file.size,
            "notified": False,
        }
    else:
        add_event("RECEIVE", f"Ready (manual download): {fname}")
        await event.reply(
            f"📥 **File Ready**\n"
            f"└ `{fname}` ({size_mb:.2f} MB)\n\n"
            f"⚠️ No download manager detected — use the buttons below:",
            buttons=buttons,
        )


# ────────────────────────────────────────────────────────
#  Callback: Button Presses
# ────────────────────────────────────────────────────────
@client.on(events.CallbackQuery(data=re.compile(b"^dl_")))
async def on_callback_query(event):
    raw = event.data.decode("utf-8")  # e.g. "dl_fdm_6161427514_521"
    parts = raw.split("_", 3)  # ["dl", "fdm", "6161427514", "521"]
    mgr_id = parts[1]  # "fdm" / "idm" / "neat" / "direct"
    chat_id = parts[2]
    msg_id = parts[3]
    link = f"http://{PROXY_HOST}:{PROXY_PORT}/dl/{chat_id}/{msg_id}"

    await event.answer()

    if mgr_id == "direct":
        # Just show the link for manual copy-paste
        await event.respond(
            f"📥 **Direct Download Link:**\n\n"
            f"`{link}`\n\n"
            f"_(Tap to copy, then paste into any download manager)_"
        )
        return

    # Attempt to trigger the specific manager
    label = MANAGER_LABELS.get(mgr_id, mgr_id.upper())

    if mgr_id not in INSTALLED_MANAGERS:
        await event.respond(
            f"⚠️ **{label} not found on this machine.**\n\n"
            f"Use the link below instead:\n`{link}`"
        )
        return

    ok = await trigger_manager(mgr_id, link)
    if ok:
        await event.respond(
            f"{label} **Download Started!**\n"
            f"└ Check your download manager — it should appear shortly.\n\n"
            f"_Backup link:_ `{link}`"
        )
    else:
        await event.respond(
            f"❌ **Failed to trigger {label}.**\n\nUse the link manually:\n`{link}`"
        )


# ────────────────────────────────────────────────────────
#  Startup
# ────────────────────────────────────────────────────────
def kill_port_owner(port: int) -> bool:
    """Find and kill the process occupying the given port. Returns True if a PID was killed."""
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        for line in result.stdout.splitlines():
            # Match lines like:  TCP  127.0.0.1:8080  ...  LISTENING  1234
            if f":{port}" in line and ("LISTENING" in line or "ESTABLISHED" in line):
                parts = line.split()
                pid = int(parts[-1])
                if pid > 0:
                    subprocess.run(
                        ["taskkill", "/F", "/PID", str(pid)],
                        capture_output=True,
                        timeout=5,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                    )
                    logger.info(
                        f"[PORT] Killed process PID {pid} that was using port {port}."
                    )
                    return True
    except Exception as e:
        logger.warning(f"[PORT] Could not kill port owner: {e}")
    return False


# ────────────────────────────────────────────────────────
#  System Tray Icon (Telegram paper-plane)
# ────────────────────────────────────────────────────────
_tray_icon = None


def _create_telegram_icon(size: int = 64, connected: bool = True):
    """Draw a Telegram-style paper plane icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Circle background
    bg_color = "#0088cc" if connected else "#6b7280"
    draw.ellipse([2, 2, size - 2, size - 2], fill=bg_color)

    # Paper plane (simplified triangle shape)
    cx, cy = size // 2, size // 2
    s = size * 0.32  # scale factor
    plane_points = [
        (cx - s, cy + s * 0.1),  # left
        (cx + s, cy),  # right tip
        (cx - s * 0.3, cy - s * 0.8),  # top
    ]
    draw.polygon(plane_points, fill="#ffffff")
    # Inner fold line
    fold_points = [
        (cx + s, cy),
        (cx - s * 0.1, cy + s * 0.4),
        (cx - s * 0.3, cy - s * 0.1),
    ]
    draw.polygon(fold_points, fill="#d4e9f7" if connected else "#9ca3af")

    return img


class LogDashboard:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def show_dashboard(cls):
        logger.info("[GUI] show_dashboard called")
        with cls._lock:
            if cls._instance is not None:
                logger.info(
                    "[GUI] LogDashboard instance already exists, calling focus()"
                )
                cls._instance.focus()
                return
            logger.info("[GUI] Creating a new LogDashboard instance")
            cls._instance = cls()
            cls._instance.start()

    def __init__(self):
        import queue

        self.queue = queue.Queue()
        self.root = None
        self.text_widget = None
        self.thread = None
        self.running = False

        # GUI Var Placeholders
        self.api_id_var = None
        self.api_hash_var = None
        self.bot_token_var = None
        self.proxy_host_var = None
        self.proxy_port_var = None
        self.minsize_var = None
        self.waitsecs_var = None
        self.allowed_ext_var = None
        self.channels_var = None
        self.keyword_block_var = None
        self.keyword_allow_var = None
        self.download_method_var = None
        self.download_dir_var = None
        self.openvpn_gui_path_var = None
        self.openvpn_profile_type_var = None
        self.openvpn_config_name_var = None
        self.lbl_custom_name = None
        self.entry_custom_name = None
        self.vpn_toggle_var = None
        self.chk_vpn = None
        self.lbl_vpn_status = None
        self.vpn_last_status = None

    def is_alive(self):
        return self.root is not None and self.running

    def focus(self):
        if self.root and self.running:
            self.queue.put((self._focus_window, ()))

    def _focus_window(self):
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

    def start(self):
        logger.info("[GUI] Starting LogDashboard GUI thread...")
        self.thread = threading.Thread(target=self._run_gui, daemon=True)
        self.thread.start()

    def _poll_queue(self):
        if not self.running or not self.root:
            return
        try:
            while not self.queue.empty():
                callback, args = self.queue.get_nowait()
                callback(*args)
        except Exception as e:
            logger.error(f"Error in queue poll: {e}")
        if self.running and self.root:
            try:
                self.root.after(50, self._poll_queue)
            except Exception:
                pass

    def _run_gui(self):
        logger.info("[GUI] GUI thread running, creating tk.Tk() instance...")
        try:
            self.root = tk.Tk()
            logger.info("[GUI] tk.Tk() instance created successfully")
        except Exception as e:
            logger.error(f"[GUI] Exception while creating tk.Tk(): {e}", exc_info=True)
            return
        self.root.title("Telegram FDM Proxy - Event Dashboard")
        self.root.configure(bg="#0d1117")
        self.root.geometry("850x580")

        self.root.option_add("*Background", "#0d1117")
        self.root.option_add("*Foreground", "#c9d1d9")

        header = tk.Frame(self.root, bg="#161b22", height=42)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text="📡 TG FDM Proxy Event Monitor (Real-time)",
            font=("Segoe UI", 10, "bold"),
            bg="#161b22",
            fg="#58a6ff",
        )
        title_label.pack(side=tk.LEFT, padx=15)

        # Navigation buttons inside header
        nav_frame = tk.Frame(header, bg="#161b22")
        nav_frame.pack(side=tk.RIGHT, padx=15)

        # VPN Controls in Header
        vpn_frame = tk.Frame(header, bg="#161b22")
        vpn_frame.pack(side=tk.RIGHT, padx=20)

        self.vpn_toggle_var = tk.BooleanVar(value=VPN_TOGGLE)
        self.chk_vpn = tk.Checkbutton(
            vpn_frame,
            text="VPN Tunnel",
            variable=self.vpn_toggle_var,
            command=self._on_vpn_toggle,
            bg="#161b22",
            fg="#c9d1d9",
            activebackground="#161b22",
            activeforeground="#c9d1d9",
            selectcolor="#0d1117",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        )
        self.chk_vpn.pack(side=tk.LEFT, padx=5)

        self.lbl_vpn_status = tk.Label(
            vpn_frame,
            text="● Disconnected",
            fg="#f85149",
            bg="#161b22",
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_vpn_status.pack(side=tk.LEFT, padx=5)

        self.btn_monitor = tk.Button(
            nav_frame,
            text="Event Monitor",
            font=("Segoe UI", 9, "bold"),
            bg="#21262d",
            fg="#58a6ff",
            activebackground="#21262d",
            activeforeground="#58a6ff",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._show_monitor,
        )
        self.btn_monitor.pack(side=tk.LEFT, padx=5)

        self.btn_settings = tk.Button(
            nav_frame,
            text="Settings",
            font=("Segoe UI", 9, "bold"),
            bg="#161b22",
            fg="#8b949e",
            activebackground="#21262d",
            activeforeground="#c9d1d9",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._show_settings,
        )
        self.btn_settings.pack(side=tk.LEFT, padx=5)

        # Main Switchable Containers
        self.main_container = tk.Frame(self.root, bg="#0d1117")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. Event Log Monitor Container
        self.monitor_frame = tk.Frame(self.main_container, bg="#0d1117")
        self.monitor_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            self.monitor_frame, bg="#0d1117", activebackground="#30363d"
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(
            self.monitor_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg="#0d1117",
            fg="#c9d1d9",
            insertbackground="white",
            selectbackground="#21262d",
            selectforeground="#c9d1d9",
            font=("Consolas", 9),
            relief=tk.FLAT,
            bd=0,
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)

        # Configure tags for category badges
        self.text_widget.tag_configure(
            "time", foreground="#8b949e", font=("Consolas", 9)
        )
        self.text_widget.tag_configure(
            "msg", foreground="#c9d1d9", font=("Segoe UI", 9)
        )

        # Badges
        self.text_widget.tag_configure(
            "badge_system", foreground="#58a6ff", font=("Consolas", 9, "bold")
        )
        self.text_widget.tag_configure(
            "badge_receive", foreground="#388bfd", font=("Consolas", 9, "bold")
        )
        self.text_widget.tag_configure(
            "badge_buffer", foreground="#d29922", font=("Consolas", 9, "bold")
        )
        self.text_widget.tag_configure(
            "badge_quality", foreground="#39d353", font=("Consolas", 9, "bold")
        )
        self.text_widget.tag_configure(
            "badge_download", foreground="#56d364", font=("Consolas", 9, "bold")
        )
        self.text_widget.tag_configure(
            "badge_error", foreground="#f85149", font=("Consolas", 9, "bold")
        )

        self.text_widget.config(state=tk.DISABLED)

        # 2. Configuration Settings Container
        self.settings_frame = tk.Frame(self.main_container, bg="#0d1117")

        panes_container = tk.Frame(self.settings_frame, bg="#0d1117")
        panes_container.pack(fill=tk.BOTH, expand=True)

        # Left Pane: Credentials & Network
        left_pane = tk.Frame(
            panes_container,
            bg="#161b22",
            highlightbackground="#30363d",
            highlightthickness=1,
        )
        left_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        left_pane.grid_columnconfigure(0, weight=1, minsize=110)
        left_pane.grid_columnconfigure(1, weight=2)

        # Right Pane: Rules & Filters
        right_pane = tk.Frame(
            panes_container,
            bg="#161b22",
            highlightbackground="#30363d",
            highlightthickness=1,
        )
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        right_pane.grid_columnconfigure(0, weight=1, minsize=170)
        right_pane.grid_columnconfigure(1, weight=2)

        # Left Pane Fields
        lbl_l_heading = tk.Label(
            left_pane,
            text="🔑 Credentials & Network",
            font=("Segoe UI", 10, "bold"),
            bg="#161b22",
            fg="#58a6ff",
        )
        lbl_l_heading.grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=15, pady=(15, 10)
        )

        # API ID
        tk.Label(
            left_pane, text="API ID:", font=("Segoe UI", 9), bg="#161b22", fg="#c9d1d9"
        ).grid(row=1, column=0, sticky=tk.W, padx=15, pady=5)
        self.api_id_var = tk.StringVar(value=str(API_ID))
        tk.Entry(
            left_pane,
            textvariable=self.api_id_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=1, column=1, sticky=tk.EW, padx=15, pady=5)

        # API Hash
        tk.Label(
            left_pane,
            text="API Hash:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=2, column=0, sticky=tk.W, padx=15, pady=5)
        self.api_hash_var = tk.StringVar(value=str(API_HASH))
        tk.Entry(
            left_pane,
            textvariable=self.api_hash_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=2, column=1, sticky=tk.EW, padx=15, pady=5)

        # Bot Token
        tk.Label(
            left_pane,
            text="Bot Token:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=3, column=0, sticky=tk.W, padx=15, pady=5)
        self.bot_token_var = tk.StringVar(value=str(BOT_TOKEN))
        tk.Entry(
            left_pane,
            textvariable=self.bot_token_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=3, column=1, sticky=tk.EW, padx=15, pady=5)

        # Proxy Host
        tk.Label(
            left_pane,
            text="Proxy Host:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=4, column=0, sticky=tk.W, padx=15, pady=5)
        self.proxy_host_var = tk.StringVar(value=str(PROXY_HOST))
        tk.Entry(
            left_pane,
            textvariable=self.proxy_host_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=4, column=1, sticky=tk.EW, padx=15, pady=5)

        # Proxy Port
        tk.Label(
            left_pane,
            text="Proxy Port:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=5, column=0, sticky=tk.W, padx=15, pady=5)
        self.proxy_port_var = tk.StringVar(value=str(PROXY_PORT))
        tk.Entry(
            left_pane,
            textvariable=self.proxy_port_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=5, column=1, sticky=tk.EW, padx=15, pady=5)

        # Download Method
        tk.Label(
            left_pane,
            text="Download Method:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=6, column=0, sticky=tk.W, padx=15, pady=5)
        self.download_method_var = tk.StringVar(value=DOWNLOAD_METHOD)
        opt_download_method = tk.OptionMenu(
            left_pane, self.download_method_var, "sequential", "parallel"
        )
        opt_download_method.config(
            bg="#21262d",
            fg="#c9d1d9",
            activebackground="#30363d",
            activeforeground="#c9d1d9",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 9),
        )
        opt_download_method["menu"].config(
            bg="#21262d",
            fg="#c9d1d9",
            activebackground="#30363d",
            activeforeground="#c9d1d9",
            relief=tk.FLAT,
            bd=0,
        )
        opt_download_method.grid(row=6, column=1, sticky=tk.EW, padx=15, pady=5)

        # Download Directory
        tk.Label(
            left_pane,
            text="Download Dir:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=7, column=0, sticky=tk.W, padx=15, pady=5)
        self.download_dir_var = tk.StringVar(value=str(DOWNLOAD_DIR))
        tk.Entry(
            left_pane,
            textvariable=self.download_dir_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=7, column=1, sticky=tk.EW, padx=15, pady=5)

        # OpenVPN GUI Path
        tk.Label(
            left_pane,
            text="OpenVPN GUI Path:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=8, column=0, sticky=tk.W, padx=15, pady=5)
        self.openvpn_gui_path_var = tk.StringVar(value=str(OPENVPN_GUI_PATH))
        tk.Entry(
            left_pane,
            textvariable=self.openvpn_gui_path_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=8, column=1, sticky=tk.EW, padx=15, pady=5)

        # OpenVPN Profile Type Dropdown
        tk.Label(
            left_pane,
            text="VPN Profile Type:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=9, column=0, sticky=tk.W, padx=15, pady=5)
        self.openvpn_profile_type_var = tk.StringVar(value=str(OPENVPN_PROFILE_TYPE))
        
        profile_options = ["US Free", "Netherlands Free", "Japan Free", "Custom Profile"]
        opt_profile_type = tk.OptionMenu(
            left_pane,
            self.openvpn_profile_type_var,
            *profile_options,
            command=self._on_profile_type_change
        )
        opt_profile_type.config(
            bg="#21262d",
            fg="#c9d1d9",
            activebackground="#30363d",
            activeforeground="#c9d1d9",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 9),
        )
        opt_profile_type["menu"].config(
            bg="#21262d",
            fg="#c9d1d9",
            activebackground="#30363d",
            activeforeground="#c9d1d9",
            relief=tk.FLAT,
            bd=0,
        )
        opt_profile_type.grid(row=9, column=1, sticky=tk.EW, padx=15, pady=5)

        # OpenVPN Custom Profile Name (initially hidden or shown based on selection)
        self.lbl_custom_name = tk.Label(
            left_pane,
            text="Custom Profile Name:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        )
        self.openvpn_config_name_var = tk.StringVar(value=str(OPENVPN_CONFIG_NAME))
        self.entry_custom_name = tk.Entry(
            left_pane,
            textvariable=self.openvpn_config_name_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        )

        # Info Label
        lbl_info = tk.Label(
            left_pane,
            text="ℹ️ Credentials, Proxy, and OpenVPN Path updates\nrequire a manual service restart to apply.",
            font=("Segoe UI", 8, "italic"),
            bg="#161b22",
            fg="#8b949e",
            justify=tk.LEFT,
        )
        lbl_info.grid(row=11, column=0, columnspan=2, sticky=tk.W, padx=15, pady=(15, 0))

        # Right Pane Fields
        lbl_r_heading = tk.Label(
            right_pane,
            text="🔍 Rules & Filtering",
            font=("Segoe UI", 10, "bold"),
            bg="#161b22",
            fg="#58a6ff",
        )
        lbl_r_heading.grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=15, pady=(15, 10)
        )

        # Min Size
        tk.Label(
            right_pane,
            text="Min File Size (MB):",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=1, column=0, sticky=tk.W, padx=15, pady=5)
        self.minsize_var = tk.StringVar(value=str(MIN_FILE_SIZE_MB))
        tk.Entry(
            right_pane,
            textvariable=self.minsize_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=1, column=1, sticky=tk.EW, padx=15, pady=5)

        # Quality Wait window
        tk.Label(
            right_pane,
            text="Wait Window (secs):",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=2, column=0, sticky=tk.W, padx=15, pady=5)
        self.waitsecs_var = tk.StringVar(value=str(QUALITY_WAIT_SECS))
        tk.Entry(
            right_pane,
            textvariable=self.waitsecs_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=2, column=1, sticky=tk.EW, padx=15, pady=5)

        # Allowed Extensions
        tk.Label(
            right_pane,
            text="Allowed Exts (e.g. .mp4,.mkv):",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=3, column=0, sticky=tk.W, padx=15, pady=5)
        self.allowed_ext_var = tk.StringVar(value=", ".join(sorted(ALLOWED_EXT)))
        tk.Entry(
            right_pane,
            textvariable=self.allowed_ext_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=3, column=1, sticky=tk.EW, padx=15, pady=5)

        # Target Channels
        tk.Label(
            right_pane,
            text="Watched Channels:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=4, column=0, sticky=tk.W, padx=15, pady=5)
        self.channels_var = tk.StringVar(
            value=", ".join(str(ch) for ch in sorted(ACTIVE_CHANNELS))
        )
        tk.Entry(
            right_pane,
            textvariable=self.channels_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=4, column=1, sticky=tk.EW, padx=15, pady=5)

        # Blocked Keywords
        tk.Label(
            right_pane,
            text="Blocked Keywords:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=5, column=0, sticky=tk.W, padx=15, pady=5)
        self.keyword_block_var = tk.StringVar(value=", ".join(sorted(KEYWORD_BLOCK)))
        tk.Entry(
            right_pane,
            textvariable=self.keyword_block_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=5, column=1, sticky=tk.EW, padx=15, pady=5)

        # Allowed Keywords
        tk.Label(
            right_pane,
            text="Allowed Keywords:",
            font=("Segoe UI", 9),
            bg="#161b22",
            fg="#c9d1d9",
        ).grid(row=6, column=0, sticky=tk.W, padx=15, pady=5)
        self.keyword_allow_var = tk.StringVar(value=", ".join(sorted(KEYWORD_ALLOW)))
        tk.Entry(
            right_pane,
            textvariable=self.keyword_allow_var,
            bg="#21262d",
            fg="#c9d1d9",
            insertbackground="white",
            relief=tk.FLAT,
            font=("Consolas", 9),
        ).grid(row=6, column=1, sticky=tk.EW, padx=15, pady=5)

        # Save Button Frame at bottom
        btn_frame = tk.Frame(self.settings_frame, bg="#0d1117")
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        btn_save = tk.Button(
            btn_frame,
            text="Save Settings",
            font=("Segoe UI", 9, "bold"),
            bg="#238636",
            fg="#ffffff",
            activebackground="#2ea043",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self._save_settings_action,
        )
        btn_save.pack(side=tk.LEFT, padx=(0, 10))

        self.save_status_label = tk.Label(
            btn_frame,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg="#0d1117",
            fg="#39d353",
        )
        self.save_status_label.pack(side=tk.LEFT, padx=10)

        self.running = True

        # DWM native rounded corners (preference 2 = round)
        self.root.update_idletasks()
        try:
            import ctypes

            hwnd = self.root.winfo_id()
            hwnd = ctypes.windll.user32.GetParent(hwnd) or hwnd
            dwmapi = ctypes.windll.dwmapi
            corner_pref = ctypes.c_int(2)
            dwmapi.DwmSetWindowAttribute(
                ctypes.c_void_p(hwnd),
                33,
                ctypes.byref(corner_pref),
                ctypes.sizeof(corner_pref),
            )
        except Exception as e:
            logger.error(f"DWM rounding error in LogDashboard: {e}")

        # Start VPN status poller thread
        threading.Thread(target=self._vpn_status_poller, daemon=True).start()

        self.root.after(100, self._poll_queue)

        # Populate history
        with EVENT_LOG_LOCK:
            for ev in EVENT_LOG:
                self._add_event_to_ui(
                    ev["time"], ev["category"], ev["message"], ev["level"]
                )

        def on_close():
            self.running = False
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        try:
            self.root.mainloop()
        except Exception:
            pass
        finally:
            self.running = False
            self.root = None
            with LogDashboard._lock:
                if LogDashboard._instance is self:
                    LogDashboard._instance = None

    def _show_monitor(self):
        if (
            self.btn_monitor
            and self.btn_settings
            and self.settings_frame
            and self.monitor_frame
        ):
            self.btn_monitor.config(fg="#58a6ff", bg="#21262d")
            self.btn_settings.config(fg="#8b949e", bg="#161b22")
            self.settings_frame.pack_forget()
            self.monitor_frame.pack(fill=tk.BOTH, expand=True)

    def _show_settings(self):
        if (
            self.btn_monitor
            and self.btn_settings
            and self.settings_frame
            and self.monitor_frame
        ):
            self.api_id_var.set(str(API_ID))
            self.api_hash_var.set(str(API_HASH))
            self.bot_token_var.set(str(BOT_TOKEN))
            self.proxy_host_var.set(str(PROXY_HOST))
            self.proxy_port_var.set(str(PROXY_PORT))
            self.minsize_var.set(str(MIN_FILE_SIZE_MB))
            self.waitsecs_var.set(str(QUALITY_WAIT_SECS))
            self.allowed_ext_var.set(", ".join(sorted(ALLOWED_EXT)))
            self.channels_var.set(", ".join(str(ch) for ch in sorted(ACTIVE_CHANNELS)))
            self.keyword_block_var.set(", ".join(sorted(KEYWORD_BLOCK)))
            self.keyword_allow_var.set(", ".join(sorted(KEYWORD_ALLOW)))
            self.download_method_var.set(DOWNLOAD_METHOD)
            self.download_dir_var.set(str(DOWNLOAD_DIR))
            self.openvpn_gui_path_var.set(str(OPENVPN_GUI_PATH))
            self.openvpn_profile_type_var.set(str(OPENVPN_PROFILE_TYPE))
            self.openvpn_config_name_var.set(str(OPENVPN_CONFIG_NAME))
            self._on_profile_type_change(OPENVPN_PROFILE_TYPE)
            self.save_status_label.config(text="")

            self.btn_settings.config(fg="#58a6ff", bg="#21262d")
            self.btn_monitor.config(fg="#8b949e", bg="#161b22")
            self.monitor_frame.pack_forget()
            self.settings_frame.pack(fill=tk.BOTH, expand=True)

    def _save_settings_action(self):
        global API_ID, API_HASH, BOT_TOKEN
        global PROXY_HOST, PROXY_PORT
        global MIN_FILE_SIZE_MB, QUALITY_WAIT_SECS
        global ALLOWED_EXT, ACTIVE_CHANNELS
        global KEYWORD_BLOCK, KEYWORD_ALLOW
        global DOWNLOAD_METHOD, DOWNLOAD_DIR
        global OPENVPN_GUI_PATH, OPENVPN_PROFILE_TYPE, OPENVPN_CONFIG_NAME

        self.save_status_label.config(text="")

        try:
            # 1. Validation
            # API ID
            api_id_raw = self.api_id_var.get().strip()
            if not api_id_raw.isdigit():
                self.save_status_label.config(
                    text="❌ API ID must be a valid integer.", fg="#f85149"
                )
                return
            new_api_id = int(api_id_raw)

            # API Hash
            new_api_hash = self.api_hash_var.get().strip()
            if not new_api_hash:
                self.save_status_label.config(
                    text="❌ API Hash cannot be empty.", fg="#f85149"
                )
                return

            # Bot Token
            new_bot_token = self.bot_token_var.get().strip()
            if not new_bot_token:
                self.save_status_label.config(
                    text="❌ Bot Token cannot be empty.", fg="#f85149"
                )
                return

            # Proxy Host
            new_proxy_host = self.proxy_host_var.get().strip()
            if not new_proxy_host:
                self.save_status_label.config(
                    text="❌ Proxy Host cannot be empty.", fg="#f85149"
                )
                return

            # Proxy Port
            proxy_port_raw = self.proxy_port_var.get().strip()
            if not proxy_port_raw.isdigit():
                self.save_status_label.config(
                    text="❌ Proxy Port must be an integer.", fg="#f85149"
                )
                return
            new_proxy_port = int(proxy_port_raw)
            if not (1 <= new_proxy_port <= 65535):
                self.save_status_label.config(
                    text="❌ Proxy Port must be between 1 and 65535.", fg="#f85149"
                )
                return

            # Min File Size
            try:
                new_min_size = float(self.minsize_var.get())
                if new_min_size <= 0:
                    raise ValueError
            except ValueError:
                self.save_status_label.config(
                    text="❌ Min file size must be > 0.", fg="#f85149"
                )
                return

            # Wait Window
            try:
                new_wait_secs = int(self.waitsecs_var.get())
                if new_wait_secs < 0:
                    raise ValueError
            except ValueError:
                self.save_status_label.config(
                    text="❌ Wait window must be >= 0.", fg="#f85149"
                )
                return

            # Allowed Extensions
            ext_raw = self.allowed_ext_var.get().strip()
            new_allowed_ext = set()
            if ext_raw:
                for e in ext_raw.split(","):
                    e = e.strip().lower()
                    if e:
                        new_allowed_ext.add(e if e.startswith(".") else f".{e}")

            # Watched Channels
            chan_raw = self.channels_var.get().strip()
            new_active_channels = set()
            if chan_raw:
                for c in chan_raw.split(","):
                    c = c.strip()
                    if not c:
                        continue
                    if c.isdigit() or (c.startswith("-") and c[1:].isdigit()):
                        new_active_channels.add(int(c))
                    else:
                        new_active_channels.add(c)

            # Blocked Keywords
            block_raw = self.keyword_block_var.get().strip()
            new_kw_block = {
                w.strip().lower() for w in block_raw.split(",") if w.strip()
            }

            # Allowed Keywords
            allow_raw = self.keyword_allow_var.get().strip()
            new_kw_allow = {
                w.strip().lower() for w in allow_raw.split(",") if w.strip()
            }

            # Download Method Validation
            new_download_method = self.download_method_var.get().strip().lower()
            if new_download_method not in ("sequential", "parallel"):
                self.save_status_label.config(
                    text="❌ Download Method must be sequential or parallel.",
                    fg="#f85149",
                )
                return

            # Download Directory Validation
            new_download_dir = self.download_dir_var.get().strip()
            if not new_download_dir:
                self.save_status_label.config(
                    text="❌ Download Directory cannot be empty.", fg="#f85149"
                )
                return

            # OpenVPN GUI Path Validation
            new_openvpn_gui_path = self.openvpn_gui_path_var.get().strip()
            if not new_openvpn_gui_path:
                self.save_status_label.config(
                    text="❌ OpenVPN GUI Path cannot be empty.", fg="#f85149"
                )
                return

            # OpenVPN Profile Type
            new_openvpn_profile_type = self.openvpn_profile_type_var.get().strip()

            # OpenVPN Config Profile
            new_openvpn_config_name = self.openvpn_config_name_var.get().strip()
            if new_openvpn_profile_type == "Custom Profile" and not new_openvpn_config_name:
                self.save_status_label.config(
                    text="❌ Custom Profile Name cannot be empty.", fg="#f85149"
                )
                return

            restart_required = False
            if (
                new_api_id != API_ID
                or new_api_hash != API_HASH
                or new_bot_token != BOT_TOKEN
                or new_proxy_host != PROXY_HOST
                or new_proxy_port != PROXY_PORT
                or new_openvpn_gui_path != OPENVPN_GUI_PATH
            ):
                restart_required = True

            # 3. Apply to in-memory variables (safely for non-restart keys)
            API_ID = new_api_id
            API_HASH = new_api_hash
            BOT_TOKEN = new_bot_token
            PROXY_HOST = new_proxy_host
            PROXY_PORT = new_proxy_port

            MIN_FILE_SIZE_MB = new_min_size
            QUALITY_WAIT_SECS = new_wait_secs
            ALLOWED_EXT = new_allowed_ext
            ACTIVE_CHANNELS = new_active_channels
            KEYWORD_BLOCK = new_kw_block
            KEYWORD_ALLOW = new_kw_allow
            DOWNLOAD_METHOD = new_download_method
            DOWNLOAD_DIR = new_download_dir
            OPENVPN_GUI_PATH = new_openvpn_gui_path
            OPENVPN_PROFILE_TYPE = new_openvpn_profile_type
            OPENVPN_CONFIG_NAME = new_openvpn_config_name

            # 4. Save to .env persistently
            config_dict = {
                "API_ID": str(API_ID),
                "API_HASH": str(API_HASH),
                "BOT_TOKEN": str(BOT_TOKEN),
                "PROXY_HOST": str(PROXY_HOST),
                "PROXY_PORT": str(PROXY_PORT),
                "MIN_FILE_SIZE_MB": f"{MIN_FILE_SIZE_MB:.1f}"
                if MIN_FILE_SIZE_MB.is_integer()
                else str(MIN_FILE_SIZE_MB),
                "QUALITY_WAIT_SECS": str(QUALITY_WAIT_SECS),
                "ALLOWED_EXT": ",".join(sorted(ALLOWED_EXT)),
                "TARGET_CHANNELS": ",".join(str(ch) for ch in sorted(ACTIVE_CHANNELS)),
                "KEYWORD_BLOCK": ",".join(sorted(KEYWORD_BLOCK)),
                "KEYWORD_ALLOW": ",".join(sorted(KEYWORD_ALLOW)),
                "DOWNLOAD_METHOD": DOWNLOAD_METHOD,
                "DOWNLOAD_DIR": DOWNLOAD_DIR,
                "OPENVPN_GUI_PATH": OPENVPN_GUI_PATH,
                "OPENVPN_PROFILE_TYPE": OPENVPN_PROFILE_TYPE,
                "OPENVPN_CONFIG_NAME": OPENVPN_CONFIG_NAME,
                "VPN_TOGGLE": str(VPN_TOGGLE),
            }

            ok = save_config_to_env(config_dict)
            if ok:
                if restart_required:
                    self.save_status_label.config(
                        text="✅ Saved! Restart FDM Proxy to apply credentials/port changes.",
                        fg="#d29922",
                    )
                    add_event(
                        "SYSTEM",
                        "Settings saved to .env (restart required for API/Proxy settings)",
                    )
                else:
                    self.save_status_label.config(
                        text="✅ Settings saved & applied dynamically!", fg="#39d353"
                    )
                    add_event("SYSTEM", "Configuration settings updated dynamically")
            else:
                self.save_status_label.config(
                    text="❌ Settings applied in memory, but failed to write to .env.",
                    fg="#d29922",
                )

        except Exception as e:
            logger.error(f"[GUI] Error saving settings: {e}")
            self.save_status_label.config(text=f"❌ Error: {e}", fg="#f85149")

    def _add_event_to_ui(self, timestamp, category, message, level):
        if not self.text_widget:
            return
        try:
            y_view = self.text_widget.yview()
            is_at_bottom = y_view[1] >= 0.95 or y_view[1] == 1.0

            self.text_widget.config(state=tk.NORMAL)

            # Print timestamp
            self.text_widget.insert(tk.END, f"[{timestamp}]", "time")

            # Print category badge
            badge_tag = f"badge_{category.lower()}"
            self.text_widget.insert(tk.END, f"  {category:<9}  ", badge_tag)

            # Print message
            msg_tag = "msg"
            if level == "error":
                msg_tag = "badge_error"
            elif level == "warning":
                msg_tag = "badge_buffer"

            self.text_widget.insert(tk.END, f" {message}\n", msg_tag)

            self.text_widget.config(state=tk.DISABLED)

            if is_at_bottom:
                self.text_widget.see(tk.END)
        except Exception as e:
            logger.debug(f"Error appending event to UI: {e}")

    def _on_vpn_toggle(self):
        val = self.vpn_toggle_var.get()
        global VPN_TOGGLE, OPENVPN_PROFILE_TYPE, OPENVPN_CONFIG_NAME, OPENVPN_GUI_PATH
        VPN_TOGGLE = val
        
        if self.openvpn_profile_type_var:
            OPENVPN_PROFILE_TYPE = self.openvpn_profile_type_var.get().strip()
        if self.openvpn_config_name_var:
            OPENVPN_CONFIG_NAME = self.openvpn_config_name_var.get().strip()
        if self.openvpn_gui_path_var:
            OPENVPN_GUI_PATH = self.openvpn_gui_path_var.get().strip()

        config_dict = {
            "VPN_TOGGLE": str(val),
            "OPENVPN_PROFILE_TYPE": OPENVPN_PROFILE_TYPE,
            "OPENVPN_CONFIG_NAME": OPENVPN_CONFIG_NAME,
            "OPENVPN_GUI_PATH": OPENVPN_GUI_PATH,
        }
        save_config_to_env(config_dict)
        
        def do_vpn_action():
            if val:
                connect_vpn_with_fallback()
            else:
                cancel_vpn_connection()
                disconnect_vpn()
        threading.Thread(target=do_vpn_action, daemon=True).start()

    def _on_profile_type_change(self, val):
        if val == "Custom Profile":
            self.lbl_custom_name.grid(row=10, column=0, sticky=tk.W, padx=15, pady=5)
            self.entry_custom_name.grid(row=10, column=1, sticky=tk.EW, padx=15, pady=5)
        else:
            self.lbl_custom_name.grid_forget()
            self.entry_custom_name.grid_forget()

    def _vpn_status_poller(self):
        """Background thread that checks VPN status every 5 seconds and updates the GUI."""
        logger.info("[VPN] Status poller thread started.")
        while self.running:
            try:
                is_connected = check_vpn_status()
                
                if self.vpn_last_status is not None and is_connected != self.vpn_last_status:
                    status_str = "connected" if is_connected else "disconnected"
                    level = "info" if is_connected else "warning"
                    add_event("VPN", f"VPN state changed: {status_str}", level)
                
                self.vpn_last_status = is_connected

                if self.root and self.running:
                    self.queue.put((self._update_vpn_gui_status, (is_connected,)))
            except Exception as e:
                logger.debug(f"Error in VPN status poller: {e}")
            
            for _ in range(50):
                if not self.running:
                    break
                time.sleep(0.1)

    def _update_vpn_gui_status(self, is_connected: bool):
        if not self.lbl_vpn_status or not self.root:
            return
        try:
            if is_connected:
                self.lbl_vpn_status.config(text="● Connected", fg="#39d353")
                self.vpn_toggle_var.set(True)
            else:
                self.lbl_vpn_status.config(text="● Disconnected", fg="#f85149")
                self.vpn_toggle_var.set(False)
        except Exception:
            pass


def _start_tray_icon():
    """Start the system tray icon in a background thread."""
    global _tray_icon
    if not TRAY_AVAILABLE:
        logger.info("[TRAY] pystray not available — running without tray icon")
        return

    def _on_quit(icon, item):
        quit_app()

    def _on_show_dashboard(icon, item):
        logger.info("[TRAY] Dashboard menu item selected")
        LogDashboard.show_dashboard()

    _tray_icon = pystray.Icon(
        "TGProxy",
        icon=_create_telegram_icon(64, True),
        title="Telegram FDM Proxy — Running",
        menu=pystray.Menu(
            pystray.MenuItem("Dashboard", _on_show_dashboard, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", _on_quit),
        ),
    )
    t = threading.Thread(target=_tray_icon.run, daemon=True)
    t.start()
    logger.info("[TRAY] Telegram tray icon started")


def _stop_tray_icon():
    global _tray_icon
    if _tray_icon:
        try:
            _tray_icon.stop()
        except Exception:
            pass
        _tray_icon = None


def quit_app():
    logger.info("Quitting Telegram FDM Proxy...")
    _stop_tray_icon()
    os._exit(0)


async def main():
    global INSTALLED_MANAGERS

    logger.info("Starting Telegram FDM Proxy")
    add_event("SYSTEM", "Starting Telegram FDM Proxy...")
    _start_tray_icon()

    # Start parent process monitoring
    system_utils.monitor_parent_process(quit_app)

    # Auto-connect VPN on startup if toggled ON
    if VPN_TOGGLE:
        logger.info("[VPN] Auto-connecting VPN on startup...")
        add_event("VPN", "Auto-connecting VPN on startup...")
        connect_vpn_with_fallback()

    # Detect download managers before connecting
    INSTALLED_MANAGERS = detect_managers()
    add_event(
        "SYSTEM",
        f"Detected download managers: {', '.join(INSTALLED_MANAGERS.keys()) if INSTALLED_MANAGERS else 'None'}",
    )

    while True:
        try:
            await client.start(bot_token=BOT_TOKEN)
            break
        except Exception as e:
            logger.warning(
                f"Connection to Telegram failed: {e}. Retrying in 10 seconds..."
            )
            add_event(
                "SYSTEM",
                f"Telegram connection failed: {e}. Retrying in 10s...",
                "warning",
            )
            await asyncio.sleep(10)
    logger.info("Bot connected successfully")
    add_event("SYSTEM", "Telegram Bot connected successfully")

    # Initialize last-seen message IDs for watched channels
    load_proxy_state()
    last_seen = proxy_state.setdefault("last_seen_message_ids", {})
    for chat_id in ACTIVE_CHANNELS:
        if str(chat_id) not in last_seen:
            await initialize_channel_state(chat_id)

    # Start network monitor task
    asyncio.create_task(_network_monitor_loop())

    # Option M: register command menu so BotFather shows it in Telegram UI
    try:
        await client(
            SetBotCommandsRequest(
                scope=BotCommandScopeDefault(),
                lang_code="",
                commands=[
                    BotCommand(
                        "start_batch", "Start collecting files for batch download"
                    ),
                    BotCommand("end_batch", "Push collected batch to download manager"),
                    BotCommand("channel", "Manage watched channels watchlist via GUI"),
                    BotCommand("channels", "List currently watched channels"),
                    BotCommand("add_channel", "Watch a new channel for auto-downloads"),
                    BotCommand("remove_channel", "Stop watching a channel"),
                    BotCommand("commands", "Show all available commands"),
                    BotCommand("help", "Show help instructions"),
                ],
            )
        )
        logger.info("[BOT] Command menu registered via setMyCommands.")
        add_event("SYSTEM", "Bot command menu registered")
    except Exception as _cmd_err:
        logger.warning(f"[BOT] Could not register command menu: {_cmd_err}")

    app = web.Application()
    app.router.add_get("/dl/{chat_id}/{message_id}", handle_download)

    runner = web.AppRunner(app)
    await runner.setup()

    # Use find_free_port() — no need to kill existing processes (from tg_fdm_proxy 1.py)
    port = find_free_port(PROXY_PORT)
    if port != PROXY_PORT:
        logger.warning(f"[PORT] {PROXY_PORT} in use, using {port} instead.")
        add_event(
            "SYSTEM", f"Port {PROXY_PORT} in use, using fallback {port}", "warning"
        )
    site = web.TCPSite(runner, PROXY_HOST, port)
    await site.start()
    add_event("SYSTEM", f"HTTP Server listening on http://{PROXY_HOST}:{port}")

    print("\n" + "=" * 52)
    print("  Telegram FDM Proxy - Running")
    print("=" * 52)
    print(f"  HTTP Server : http://{PROXY_HOST}:{port}")
    if INSTALLED_MANAGERS:
        for mgr, path in INSTALLED_MANAGERS.items():
            short = os.path.basename(path)
            print(f"  {mgr.upper():<6} : {short}")
    else:
        print("  No download managers detected")
    if ALLOWED_EXT:
        print(f"  Filter  : {', '.join(sorted(ALLOWED_EXT))}")
    print(f"  Min Size: {MIN_FILE_SIZE_MB} MB")
    print("  Forward a Telegram file to your bot to start")
    print("=" * 52 + "\n")

    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("\nStopping proxy...")
    finally:
        await site.stop()
        await runner.cleanup()
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProxy stopped.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
