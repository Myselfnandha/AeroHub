"""
Media Control — Taskbar Tray Controls only.
Uses Windows SDK (winsdk) for real-time media session status, and Win32 APIs
to display 3 interactive system tray control icons.
"""

import os
import sys
import ctypes
import ctypes.wintypes
import threading
import logging
import logging.handlers
import time
import asyncio
import winreg
from PIL import Image, ImageDraw

# Win32 modules
import win32gui
import win32con

# ── AeroHub Theme ──
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg_card": "#1a1a3e",
    "accent": "#7c3aed",
    "accent_hover": "#9b59f5",
    "success": "#00ff88",
    "danger": "#ff3366",
    "warning": "#ffdd00",
    "fg": "#f0f0f0",
    "fg_dim": "#6a7080",
    "border": "#2d2d5e",
    "running": "#00ff88",
    "stopped": "#ff3366",
}


def get_friendly_app_name(app_id: str) -> str:
    if not app_id:
        return "Unknown"

    app_id = str(app_id)
    name = app_id

    # 1. Handle UWP Packaged Apps (e.g. SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify)
    if "!" in app_id:
        name = app_id.split("!")[-1]
        if name.lower() == "app" and "." in app_id:
            name = app_id.split(".")[1] if len(app_id.split(".")) > 1 else name
    # 2. Handle file paths (e.g. C:\...\vlc.exe)
    elif "\\" in app_id or "/" in app_id:
        file_name = app_id.replace("\\", "/").split("/")[-1]
        name = file_name.split(".")[0] if "." in file_name else file_name
    # 3. Handle dot-separated AUMIDs (e.g. Mozilla.Firefox.308046B0AF4A39CB)
    elif "." in app_id and not app_id.lower().endswith(".exe"):
        parts = app_id.split(".")
        if len(parts) >= 2:
            name = parts[1]
    # 4. Fallback for things like 'chrome.exe'
    elif app_id.lower().endswith(".exe"):
        name = app_id[:-4]

    name = name.capitalize()

    # Prettify common names
    name_lower = name.lower()
    if name_lower == "chrome":
        return "Google Chrome"
    if name_lower == "msedge" or name_lower == "edge":
        return "Microsoft Edge"
    if name_lower == "vlc":
        return "VLC Media Player"

    return name


# ── WNDPROC & WNDCLASSW ctypes definitions for 64-bit safety ──
WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.wintypes.LPARAM,  # LRESULT is LPARAM
    ctypes.wintypes.HWND,
    ctypes.wintypes.UINT,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
)


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", ctypes.c_uint),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", ctypes.wintypes.HANDLE),
        ("hIcon", ctypes.wintypes.HANDLE),
        ("hCursor", ctypes.wintypes.HANDLE),
        ("hbrBackground", ctypes.wintypes.HANDLE),
        ("lpszMenuName", ctypes.wintypes.LPCWSTR),
        ("lpszClassName", ctypes.wintypes.LPCWSTR),
    ]


try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    )
except ImportError:
    print("winsdk library is missing. Install with: pip install winsdk")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
LOG_PATH = os.path.join(ROOT_DIR, "media_control.log")
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Ensure workspace root is in sys.path to import system_utils
WORKSPACE_ROOT = os.path.dirname(ROOT_DIR)
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
import system_utils

# Set unique AppUserModelID so tray icons appear separately
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "AeroHub.MediaControl"
    )
except Exception:
    pass

# ── Logging ──
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
logger = logging.getLogger("MediaControl")

# ── Configuration & Win32 Constants ──
ICON_SIZE = 32
EXIT_CMD_ID = 1001
DASHBOARD_CMD_ID = 1002
WM_TRAY = win32con.WM_USER + 20

VK_MEDIA_NEXT = 0xB0
VK_MEDIA_PREV = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3


def send_media_key(vk_code: int):
    """Simulate a media key press and release globally via keybd_event."""
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)


# ── Windows Theme Detection ──
def is_light_mode() -> bool:
    try:
        path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
        color_prevalence, _ = winreg.QueryValueEx(key, "ColorPrevalence")
        system_light, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")

        if color_prevalence == 1:
            dwm_path = r"Software\Microsoft\Windows\DWM"
            dwm_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, dwm_path)
            try:
                accent, _ = winreg.QueryValueEx(dwm_key, "AccentColor")
                r = accent & 0xFF
                g = (accent >> 8) & 0xFF
                b = (accent >> 16) & 0xFF
            except Exception:
                colorization, _ = winreg.QueryValueEx(dwm_key, "ColorizationColor")
                r = (colorization >> 16) & 0xFF
                g = (colorization >> 8) & 0xFF
                b = colorization & 0xFF

            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            return luminance > 140

        return system_light == 1
    except Exception:
        return False


def get_theme_color() -> str:
    return "#000000" if is_light_mode() else "#FFFFFF"


# ── Windows Icon Generator (HICON) ──
def create_hicon(icon_type: str, color_hex: str, clicked: bool = False):
    """Creates a Windows HICON from a dynamically drawn PIL image with a rounded box background."""
    scale = 4
    s = ICON_SIZE * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = int(8 * scale)  # Modern Fluent corner rounding
    margin = int(2 * scale)
    click_scale = 0.86 if clicked else 1.0

    is_light = is_light_mode()

    if clicked:
        box_bg = (0, 120, 215, int(160 * click_scale))  # Fluent active accent blue
        box_outline = (0, 120, 215, int(230 * click_scale))
        symbol_color = (255, 255, 255, 255)
    else:
        if is_light:
            box_bg = (0, 0, 0, 12)  # Fluent translucent light
            box_outline = (0, 0, 0, 20)
            symbol_color = (30, 30, 30, 255)
        else:
            box_bg = (255, 255, 255, 14)  # Fluent translucent dark
            box_outline = (255, 255, 255, 30)
            symbol_color = (240, 240, 240, 255)

    # Apply click scale
    box_size = s - 2 * margin
    scaled_box_size = int(box_size * click_scale)
    pad = (s - scaled_box_size) // 2

    left = pad
    top = pad
    right = s - pad
    bottom = s - pad

    # Standalone capsules matching Windows 11 style (no joined cut-off segments)
    draw_left = left
    draw_right = right
    visible_left = left
    visible_right = right

    draw.rounded_rectangle(
        [draw_left, top, draw_right, bottom],
        radius=int(radius * click_scale),
        fill=box_bg,
        outline=box_outline,
        width=int(1.5 * scale),
    )

    cx = (visible_left + visible_right) // 2
    cy = s // 2
    m = 4.3 * click_scale

    if icon_type == "play":
        draw.polygon(
            [(cx - 5 * m, cy - 9 * m), (cx - 5 * m, cy + 9 * m), (cx + 9 * m, cy)],
            fill=symbol_color,
        )
    elif icon_type == "pause":
        draw.rectangle(
            [cx - 7 * m, cy - 8 * m, cx - 2 * m, cy + 8 * m], fill=symbol_color
        )
        draw.rectangle(
            [cx + 2 * m, cy - 8 * m, cx + 7 * m, cy + 8 * m], fill=symbol_color
        )
    elif icon_type == "prev":
        draw.rectangle(
            [cx - 10 * m, cy - 7 * m, cx - 7 * m, cy + 7 * m], fill=symbol_color
        )
        draw.polygon(
            [(cx + 9 * m, cy - 9 * m), (cx + 9 * m, cy + 9 * m), (cx - 5 * m, cy)],
            fill=symbol_color,
        )
    elif icon_type == "next":
        draw.polygon(
            [(cx - 9 * m, cy - 9 * m), (cx - 9 * m, cy + 9 * m), (cx + 5 * m, cy)],
            fill=symbol_color,
        )
        draw.rectangle(
            [cx + 7 * m, cy - 7 * m, cx + 10 * m, cy + 7 * m], fill=symbol_color
        )

    img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)

    # Save to temp file to create HICON
    import tempfile

    fd, path = tempfile.mkstemp(suffix=".ico", prefix=f"media_{icon_type}_")
    os.close(fd)
    try:
        img.save(path)
        hicon = win32gui.LoadImage(
            0, path, win32con.IMAGE_ICON, ICON_SIZE, ICON_SIZE, win32con.LR_LOADFROMFILE
        )
    finally:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    return hicon


# ══════════════════════════════════════════════════════════
#  Media Control App Class
# ══════════════════════════════════════════════════════════
class MediaControlApp:
    def __init__(self):
        self.active_hicons = {}
        self.clicking_states = {}
        self.theme_color = get_theme_color()
        self.current_play_type = "play"
        self.icon_lock = threading.Lock()

        self.controls = [
            {
                "id": 1,
                "type": "prev",
                "tip": "Previous Track",
                "cmd": lambda: send_media_key(VK_MEDIA_PREV),
            },
            {
                "id": 2,
                "type": "play",
                "tip": "Play/Pause",
                "cmd": self.handle_play_pause,
            },
            {
                "id": 3,
                "type": "next",
                "tip": "Next Track",
                "cmd": lambda: send_media_key(VK_MEDIA_NEXT),
            },
        ]

        self.current_status = None
        self.current_title = ""
        self.current_artist = ""

        self.active_sessions = []
        self.active_sessions_count = 0

        self.update_event = None
        self.async_loop = None

        # Start Win32 Tray Loop in background thread
        self.start_tray_thread()

        # Start Media Monitor Thread
        self.start_monitor()

        # Start parent process monitoring
        system_utils.monitor_parent_process(self.quit_app)

    def start_tray_thread(self):
        self.window_ready_event = threading.Event()
        t = threading.Thread(target=self.run_tray_loop, daemon=True)
        t.start()
        self.window_ready_event.wait(timeout=2.0)

    def run_tray_loop(self):
        self._init_cached_icons()
        self.hwnd = self._init_window()
        self._create_tray_icons()
        self.window_ready_event.set()
        self.run_win32_msg_loop()

    def run_win32_msg_loop(self):
        user32 = ctypes.windll.user32
        user32.GetMessageW.restype = ctypes.wintypes.BOOL
        user32.GetMessageW.argtypes = [
            ctypes.POINTER(ctypes.wintypes.MSG),
            ctypes.wintypes.HWND,
            ctypes.wintypes.UINT,
            ctypes.wintypes.UINT,
        ]
        user32.TranslateMessage.restype = ctypes.wintypes.BOOL
        user32.TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]
        user32.DispatchMessageW.restype = ctypes.wintypes.LPARAM
        user32.DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def _init_cached_icons(self):
        with self.icon_lock:
            self._cleanup_cached_icons_unlocked()
            self.theme_color = get_theme_color()
            self.cached_icons = {}
            for icon_type in ["prev", "play", "pause", "next"]:
                self.cached_icons[icon_type] = {
                    "normal": create_hicon(icon_type, self.theme_color, clicked=False),
                    "clicked": create_hicon(icon_type, self.theme_color, clicked=True),
                }

    def _cleanup_cached_icons_unlocked(self):
        if not hasattr(self, "cached_icons"):
            return
        for icon_type, states in self.cached_icons.items():
            for state, hicon in states.items():
                if hicon:
                    try:
                        win32gui.DestroyIcon(hicon)
                    except Exception:
                        pass
        self.cached_icons = {}

    def _cleanup_cached_icons(self):
        with self.icon_lock:
            self._cleanup_cached_icons_unlocked()

    def _init_window(self):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # Setup ctypes function signatures for 64-bit safety
        kernel32.GetModuleHandleW.restype = ctypes.wintypes.HANDLE
        kernel32.GetModuleHandleW.argtypes = [ctypes.wintypes.LPCWSTR]

        user32.RegisterClassW.restype = ctypes.wintypes.ATOM
        user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]

        user32.CreateWindowExW.restype = ctypes.wintypes.HWND
        user32.CreateWindowExW.argtypes = [
            ctypes.wintypes.DWORD,
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.wintypes.HWND,
            ctypes.wintypes.HMENU,
            ctypes.wintypes.HANDLE,
            ctypes.c_void_p,
        ]

        user32.DefWindowProcW.restype = ctypes.wintypes.LPARAM
        user32.DefWindowProcW.argtypes = [
            ctypes.wintypes.HWND,
            ctypes.wintypes.UINT,
            ctypes.wintypes.WPARAM,
            ctypes.wintypes.LPARAM,
        ]

        user32.PostQuitMessage.restype = None
        user32.PostQuitMessage.argtypes = [ctypes.c_int]

        # Bind the wndproc callback to an instance attribute to prevent GC
        def wnd_proc(hwnd, msg, wparam, lparam):
            try:
                return self._handle_window_msg(hwnd, msg, wparam, lparam)
            except Exception as e:
                logger.exception(f"Unhandled exception in wnd_proc callback: {e}")
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        self._wnd_proc = WNDPROC(wnd_proc)

        hInstance = kernel32.GetModuleHandleW(None)

        wc = WNDCLASSW()
        wc.style = 0
        wc.lpfnWndProc = self._wnd_proc
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = hInstance
        wc.hIcon = None
        wc.hCursor = None
        wc.hbrBackground = None
        wc.lpszMenuName = None
        wc.lpszClassName = "MediaControlTrayWinClass"

        user32.RegisterClassW(ctypes.byref(wc))

        hwnd = user32.CreateWindowExW(
            0,
            wc.lpszClassName,
            "MediaControlTrayHandler",
            0,
            0,
            0,
            0,
            0,
            None,
            None,
            hInstance,
            None,
        )
        if not hwnd:
            logger.error("Failed to create tray window using CreateWindowExW")
        return hwnd

    def _handle_window_msg(self, hwnd, msg, wparam, lparam):
        try:
            if msg == WM_TRAY:
                if lparam == win32con.WM_LBUTTONDOWN:
                    self._trigger_click_effect(wparam)
                    count = getattr(self, "active_sessions_count", 0)
                    logger.info(
                        f"Tray icon clicked. Control ID: {wparam}, Active Sessions Count: {count}"
                    )
                    logger.info("Executing standard media key command...")
                    for ctrl in self.controls:
                        if ctrl["id"] == wparam:
                            ctrl["cmd"]()
                            break
                elif lparam == win32con.WM_RBUTTONUP:
                    self.show_context_menu()
            elif msg == win32con.WM_COMMAND:
                if wparam == EXIT_CMD_ID:
                    self.quit_app()
            elif msg == win32con.WM_DESTROY:
                ctypes.windll.user32.PostQuitMessage(0)
                return 0

            user32 = ctypes.windll.user32
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        except Exception as e:
            logger.exception(f"Error in window procedure: {e}")
            return 0

    def show_context_menu(self):
        cursor_x, cursor_y = win32gui.GetCursorPos()
        hmenu = win32gui.CreatePopupMenu()
        win32gui.AppendMenu(hmenu, win32con.MF_STRING, EXIT_CMD_ID, "Exit")

        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(
            hmenu,
            win32con.TPM_LEFTALIGN | win32con.TPM_RIGHTBUTTON,
            cursor_x,
            cursor_y,
            0,
            self.hwnd,
            None,
        )
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        win32gui.DestroyMenu(hmenu)

    def handle_play_pause(self):
        playing_sessions = [
            s for s in getattr(self, "active_sessions", []) if s["status"] == 4
        ]
        if len(playing_sessions) > 1:
            logger.info("Multiple sessions playing. Pausing all.")
            for session in playing_sessions:
                app_id = session["app_id"]
                is_pycaw = session.get("is_pycaw", False)
                if is_pycaw:
                    self.send_pycaw_command(app_id, "pause")
                else:
                    self.send_session_command(app_id, "pause")
        else:
            logger.info(
                "Single session playing/paused or all paused. Sending global play/pause."
            )
            send_media_key(VK_MEDIA_PLAY_PAUSE)

    def _trigger_click_effect(self, ctrl_id):
        if self.clicking_states.get(ctrl_id):
            return
        self.clicking_states[ctrl_id] = True

        # Find control type
        ctrl_type = None
        for ctrl in self.controls:
            if ctrl["id"] == ctrl_id:
                ctrl_type = ctrl["type"]
                break
        if not ctrl_type:
            self.clicking_states[ctrl_id] = False
            return

        with self.icon_lock:
            clicked_hicon = self.cached_icons[ctrl_type]["clicked"]
        self._update_tray_icon(ctrl_id, clicked_hicon)

        def revert():
            time.sleep(0.12)
            current_ctrl_type = None
            for ctrl in self.controls:
                if ctrl["id"] == ctrl_id:
                    current_ctrl_type = ctrl["type"]
                    break
            if current_ctrl_type:
                with self.icon_lock:
                    if current_ctrl_type in self.cached_icons:
                        normal_hicon = self.cached_icons[current_ctrl_type]["normal"]
                        self._update_tray_icon(ctrl_id, normal_hicon)
            self.clicking_states[ctrl_id] = False

        threading.Thread(target=revert, daemon=True).start()

    def _create_tray_icons(self):
        # Windows tray adds icons right-to-left, so create in reverse
        # order to get: Previous | Play/Pause | Next (left to right)
        for ctrl in reversed(self.controls):
            with self.icon_lock:
                hicon = self.cached_icons[ctrl["type"]]["normal"]
            self.active_hicons[ctrl["id"]] = hicon
            flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
            win32gui.Shell_NotifyIcon(
                win32gui.NIM_ADD,
                (self.hwnd, ctrl["id"], flags, WM_TRAY, hicon, ctrl["tip"]),
            )
            time.sleep(0.1)

    def _update_tray_icon(self, icon_id, hicon):
        if self.active_hicons.get(icon_id) == hicon:
            return
        self.active_hicons[icon_id] = hicon
        win32gui.Shell_NotifyIcon(
            win32gui.NIM_MODIFY,
            (self.hwnd, icon_id, win32gui.NIF_ICON, WM_TRAY, hicon, ""),
        )

    def update_play_pause_icon(self, status):
        """Update the Play/Pause icon depending on active playback state."""
        play_type = "pause" if status == 4 else "play"
        if play_type != self.current_play_type:
            self.current_play_type = play_type
            for ctrl in self.controls:
                if ctrl["id"] == 2:
                    ctrl["type"] = play_type
                    with self.icon_lock:
                        hicon = self.cached_icons[play_type]["normal"]
                    self._update_tray_icon(2, hicon)

    def check_theme_update(self):
        """Update all icons if the OS theme color shifts."""
        current_color = get_theme_color()
        if current_color != self.theme_color:
            logger.info("Theme change detected, rebuilding tray icons...")
            self._init_cached_icons()
            for ctrl in self.controls:
                with self.icon_lock:
                    hicon = self.cached_icons[ctrl["type"]]["normal"]
                self._update_tray_icon(ctrl["id"], hicon)

    def shutdown(self):
        """Gracefully delete notification tray icons and release GDI objects."""
        for ctrl in self.controls:
            try:
                win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (self.hwnd, ctrl["id"]))
            except Exception:
                pass

        self._cleanup_cached_icons()

        try:
            user32 = ctypes.windll.user32
            user32.DestroyWindow.restype = ctypes.wintypes.BOOL
            user32.DestroyWindow.argtypes = [ctypes.wintypes.HWND]
            user32.DestroyWindow(self.hwnd)
        except Exception:
            pass

    # ── Media Monitor (Winsdk Session Manager) ──
    def start_monitor(self):
        self.monitor_thread = threading.Thread(
            target=self.run_monitor_loop, daemon=True
        )
        self.monitor_thread.start()

    def run_monitor_loop(self):
        # Initialize COM as MTA for this thread to support WinRT calls safely
        hr = ctypes.windll.ole32.CoInitializeEx(None, 2)
        logger.info(f"CoInitializeEx returned {hr}")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.async_loop = loop
            self.update_event = asyncio.Event()
            loop.run_until_complete(self.monitor_media())
        finally:
            if hr == 0 or hr == 1:
                ctypes.windll.ole32.CoUninitialize()

    async def monitor_media(self):
        manager = None
        while manager is None:
            try:
                manager = await SessionManager.request_async()
            except Exception as e:
                logger.error(
                    f"Failed to request winsdk SessionManager: {e}. Retrying in 5s..."
                )
                await asyncio.sleep(5)

        while True:
            session = None
            info = None
            try:
                session = manager.get_current_session()
                if session:
                    info = session.get_playback_info()
                    status = info.playback_status if info else None

                    title = ""
                    artist = ""
                    try:
                        props = await session.try_get_media_properties_async()
                        if props:
                            title = props.title or ""
                            artist = props.artist or ""
                    except Exception as pe:
                        logger.debug(f"Failed to get media properties: {pe}")

                    if (
                        status != self.current_status
                        or title != self.current_title
                        or artist != self.current_artist
                    ):
                        self.current_status = status
                        self.current_title = title
                        self.current_artist = artist
                        self.update_media_state(status, title, artist)
                else:
                    if (
                        self.current_status is not None
                        or self.current_title != ""
                        or self.current_artist != ""
                    ):
                        self.current_status = None
                        self.current_title = ""
                        self.current_artist = ""
                        self.update_media_state(None, "", "")

                # Multi-session monitoring — always count active sessions
                active_sessions_list = []
                smtc_sessions = manager.get_sessions()
                for s in smtc_sessions:
                    try:
                        s_app_id = s.source_app_user_model_id
                        s_info = s.get_playback_info()
                        s_status = s_info.playback_status if s_info else 0

                        if s_status in (3, 4, 5):  # Stopped, Playing, or Paused
                            s_props = await s.try_get_media_properties_async()
                            s_title = s_props.title if s_props else ""
                            s_artist = s_props.artist if s_props else ""

                            # Filter out ghost/zombie sessions
                            if not s_app_id and not s_title and not s_artist:
                                continue

                            # Deduplicate identical SMTC sessions (browsers sometimes register twice)
                            is_duplicate = False
                            for existing in active_sessions_list:
                                if existing.get("app_id") == s_app_id:
                                    is_duplicate = True
                                    break

                            if not is_duplicate:
                                active_sessions_list.append(
                                    {
                                        "app_id": s_app_id or "UnknownApp",
                                        "status": s_status,
                                        "title": s_title,
                                        "artist": s_artist,
                                    }
                                )
                    except Exception as se:
                        logger.debug(f"Failed to query individual session: {se}")

                # --- PYCAW FALLBACK FOR NON-SMTC AUDIO ---
                try:
                    from pycaw.pycaw import AudioUtilities

                    pycaw_sessions = AudioUtilities.GetAllSessions()
                    for s in pycaw_sessions:
                        try:
                            if not s.Process:
                                continue
                            proc_name = s.Process.name()
                            lower_name = proc_name.lower()
                            # Ignore system/self/background
                            if any(
                                x in lower_name
                                for x in [
                                    "svchost",
                                    "health_app",
                                    "python",
                                    "antigravity",
                                    "system",
                                    "idle",
                                ]
                            ):
                                continue

                            # ONLY fallback for known media players that break SMTC (e.g. VLC, MPC-HC, iTunes)
                            known_players = [
                                "vlc",
                                "mpc-hc",
                                "itunes",
                                "winamp",
                                "wmplayer",
                                "potplayermini64",
                            ]
                            if not any(x in lower_name for x in known_players):
                                continue

                            # Check if this app is already represented in SMTC list
                            friendly = get_friendly_app_name(proc_name)
                            already_in_smtc = False
                            for d in active_sessions_list:
                                d_friendly = get_friendly_app_name(d["app_id"])
                                if (
                                    friendly.lower() in d_friendly.lower()
                                    or d_friendly.lower() in friendly.lower()
                                ):
                                    already_in_smtc = True
                                    break

                            if not already_in_smtc:
                                status = (
                                    4 if s.State == 1 else 5
                                )  # 1=Active(Playing), 0=Inactive(Paused)
                                # Only show pycaw sessions that are actually actively playing sound
                                if status == 4:
                                    active_sessions_list.append(
                                        {
                                            "app_id": proc_name,
                                            "status": status,
                                            "title": f"{friendly} Audio",
                                            "artist": "Local Media",
                                            "is_pycaw": True,
                                        }
                                    )
                        except Exception:
                            pass
                except ImportError:
                    pass
                except Exception as pycaw_e:
                    logger.debug(f"Pycaw fallback failed: {pycaw_e}")

                new_count = len(active_sessions_list)
                self.active_sessions = active_sessions_list
                self.active_sessions_count = new_count

                if new_count != getattr(self, "prev_active_count", -1):
                    logger.info(f"Active sessions count changed to: {new_count}")
                    self.prev_active_count = new_count

            except Exception as e:
                logger.error(f"Error checking Windows Media session: {e}")
            finally:
                if session is not None:
                    del session
                if info is not None:
                    del info
                import gc

                gc.collect()

            try:
                await asyncio.wait_for(self.update_event.wait(), timeout=0.5)
                self.update_event.clear()
            except asyncio.TimeoutError:
                pass

    def update_media_state(self, status, title="", artist=""):
        self.update_play_pause_icon(status)
        self.check_theme_update()
        self.update_tooltips(status, title, artist)

    def update_tooltips(self, status, title="", artist=""):
        """Update the tooltips of all icons dynamically based on playing media."""
        if title:
            track_info = f"\nTrack: {title}"
            if artist:
                track_info += f" - {artist}"
        else:
            track_info = ""

        status_desc = (
            "Playing" if status == 4 else "Paused" if status in (3, 5) else "Idle"
        )

        if track_info:
            play_tip = f"Media Control ({status_desc}){track_info}"
        else:
            play_tip = "Media Control (Play/Pause)"

        if len(play_tip) > 127:
            play_tip = play_tip[:124] + "..."

        prev_tip = "Previous Track"
        next_tip = "Next Track"

        for ctrl in self.controls:
            tip = (
                play_tip
                if ctrl["type"] in ("play", "pause")
                else prev_tip
                if ctrl["type"] == "prev"
                else next_tip
            )
            ctrl["tip"] = tip
            try:
                hicon = self.active_hicons.get(ctrl["id"])
                if hicon:
                    win32gui.Shell_NotifyIcon(
                        win32gui.NIM_MODIFY,
                        (self.hwnd, ctrl["id"], win32gui.NIF_TIP, WM_TRAY, hicon, tip),
                    )
            except Exception as e:
                logger.debug(f"Failed to update tooltip for control {ctrl['id']}: {e}")

    def send_session_command(self, app_id, command):
        if not self.async_loop:
            return

        async def run_cmd():
            try:
                manager = await SessionManager.request_async()
                sessions = manager.get_sessions()
                for s in sessions:
                    try:
                        s_app_id = s.source_app_user_model_id
                        if s_app_id == app_id:
                            if command == "play":
                                await s.try_play_async()
                            elif command == "pause":
                                await s.try_pause_async()
                            elif command == "next":
                                await s.try_skip_next_async()
                            elif command == "prev":
                                await s.try_skip_previous_async()
                            break  # Found and executed
                    except Exception as e:
                        logger.debug(f"Error checking session for {app_id}: {e}")
            except Exception as e:
                logger.error(f"Error sending session command {command}: {e}")

        asyncio.run_coroutine_threadsafe(run_cmd(), self.async_loop)

    def send_pycaw_command(self, process_name, command):
        import win32gui
        import win32process
        import psutil

        WM_APPCOMMAND = 0x0319
        cmd_map = {
            "play": 14,  # APPCOMMAND_MEDIA_PLAY_PAUSE
            "pause": 47,  # APPCOMMAND_MEDIA_PAUSE
            "next": 11,  # APPCOMMAND_MEDIA_NEXTTRACK
            "prev": 12,  # APPCOMMAND_MEDIA_PREVIOUSTRACK
        }

        if command not in cmd_map:
            return

        app_cmd = cmd_map[command]

        try:
            hwnds = []

            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    hwnds.append((hwnd, pid))
                return True

            win32gui.EnumWindows(callback, hwnds)
            target_pids = set(
                p.pid
                for p in psutil.process_iter(["name"])
                if p.info["name"] and p.info["name"].lower() == process_name.lower()
            )

            target_hwnds = [hwnd for hwnd, pid in hwnds if pid in target_pids]
            if target_hwnds:
                # Send command to the first visible window of the target process
                win32gui.PostMessage(target_hwnds[0], WM_APPCOMMAND, 0, app_cmd << 16)
                self.trigger_immediate_update()
        except Exception as e:
            logger.error(f"Error sending pycaw command: {e}")

    def trigger_immediate_update(self):
        if self.update_event and self.async_loop:
            self.async_loop.call_soon_threadsafe(self.update_event.set)

    def run(self):
        try:
            import time

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.quit_app()

    def quit_app(self):
        logger.info("Gracefully quitting Media Control application...")
        self.shutdown()
        os._exit(0)


if __name__ == "__main__":
    app = MediaControlApp()
    app.run()
