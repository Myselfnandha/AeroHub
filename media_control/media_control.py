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
import win32api
import win32con

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
        ('style', ctypes.c_uint),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', ctypes.wintypes.HANDLE),
        ('hIcon', ctypes.wintypes.HANDLE),
        ('hCursor', ctypes.wintypes.HANDLE),
        ('hbrBackground', ctypes.wintypes.HANDLE),
        ('lpszMenuName', ctypes.wintypes.LPCWSTR),
        ('lpszClassName', ctypes.wintypes.LPCWSTR),
    ]


try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
        GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
    )
except ImportError:
    print("winsdk library is missing. Install with: pip install winsdk")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(SCRIPT_DIR, "media_control.log")
os.makedirs(SCRIPT_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icons appear separately
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.MediaControl")
except Exception:
    pass

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("MediaControl")

# ── Configuration & Win32 Constants ──
ICON_SIZE = 32
EXIT_CMD_ID = 1001
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
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    radius = int(18 * scale)
    margin = int(2 * scale)
    click_scale = 0.86 if clicked else 1.0
    
    is_light = is_light_mode()
    
    if clicked:
        box_bg = (0, 122, 255, int(140 * click_scale))  # iOS active blue
        box_outline = (0, 122, 255, int(240 * click_scale))
        symbol_color = (255, 255, 255, 255)
    else:
        if is_light:
            box_bg = (0, 0, 0, 16)          # iOS water translucent light
            box_outline = (0, 0, 0, 32)
            symbol_color = (0, 0, 0, 210)
        else:
            box_bg = (255, 255, 255, 20)   # iOS water translucent dark
            box_outline = (255, 255, 255, 60)
            symbol_color = (255, 255, 255, 245)
            
    # Apply click scale
    box_size = s - 2 * margin
    scaled_box_size = int(box_size * click_scale)
    pad = (s - scaled_box_size) // 2
    
    left = pad
    top = pad
    right = s - pad
    bottom = s - pad
    
    # Custom corner joining styles (iOS-style segmented control)
    if icon_type == "prev":
        draw_left = left
        draw_right = s + radius
        visible_left = left
        visible_right = s
    elif icon_type == "next":
        draw_left = -radius
        draw_right = right
        visible_left = 0
        visible_right = right
    else:  # play / pause
        draw_left = -radius
        draw_right = s + radius
        visible_left = 0
        visible_right = s

    draw.rounded_rectangle(
        [draw_left, top, draw_right, bottom],
        radius=int(radius * click_scale),
        fill=box_bg,
        outline=box_outline,
        width=3
    )
    
    cx = (visible_left + visible_right) // 2
    cy = s // 2
    m = 4.3 * click_scale
    
    if icon_type == "play":
        draw.polygon([(cx - 5*m, cy - 9*m), (cx - 5*m, cy + 9*m), (cx + 9*m, cy)], fill=symbol_color)
    elif icon_type == "pause":
        draw.rectangle([cx - 7*m, cy - 8*m, cx - 2*m, cy + 8*m], fill=symbol_color)
        draw.rectangle([cx + 2*m, cy - 8*m, cx + 7*m, cy + 8*m], fill=symbol_color)
    elif icon_type == "prev":
        draw.rectangle([cx - 10*m, cy - 7*m, cx - 7*m, cy + 7*m], fill=symbol_color)
        draw.polygon([(cx + 9*m, cy - 9*m), (cx + 9*m, cy + 9*m), (cx - 5*m, cy)], fill=symbol_color)
    elif icon_type == "next":
        draw.polygon([(cx - 9*m, cy - 9*m), (cx - 9*m, cy + 9*m), (cx + 5*m, cy)], fill=symbol_color)
        draw.rectangle([cx + 7*m, cy - 7*m, cx + 10*m, cy + 7*m], fill=symbol_color)
        
    img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    
    # Save to temp file to create HICON
    import tempfile
    fd, path = tempfile.mkstemp(suffix=".ico", prefix=f"media_{icon_type}_")
    os.close(fd)
    try:
        img.save(path)
        hicon = win32gui.LoadImage(0, path, win32con.IMAGE_ICON, ICON_SIZE, ICON_SIZE, win32con.LR_LOADFROMFILE)
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
                "cmd": lambda: send_media_key(VK_MEDIA_PREV)
            },
            {
                "id": 2,
                "type": "play",
                "tip": "Play/Pause",
                "cmd": lambda: send_media_key(VK_MEDIA_PLAY_PAUSE)
            },
            {
                "id": 3,
                "type": "next",
                "tip": "Next Track",
                "cmd": lambda: send_media_key(VK_MEDIA_NEXT)
            }
        ]
        
        self.current_status = None
        
        # Initialize cached icons first
        self._init_cached_icons()
        
        # Initialize message-handling window
        self.hwnd = self._init_window()
        self._create_tray_icons()
        
        # Start Media Monitor Thread
        self.start_monitor()

    def _init_cached_icons(self):
        with self.icon_lock:
            self._cleanup_cached_icons_unlocked()
            self.theme_color = get_theme_color()
            self.cached_icons = {}
            for icon_type in ["prev", "play", "pause", "next"]:
                self.cached_icons[icon_type] = {
                    "normal": create_hicon(icon_type, self.theme_color, clicked=False),
                    "clicked": create_hicon(icon_type, self.theme_color, clicked=True)
                }

    def _cleanup_cached_icons_unlocked(self):
        if not hasattr(self, 'cached_icons'):
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
            ctypes.wintypes.DWORD, ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.wintypes.HWND, ctypes.wintypes.HMENU, ctypes.wintypes.HANDLE, ctypes.c_void_p
        ]

        user32.DefWindowProcW.restype = ctypes.wintypes.LPARAM
        user32.DefWindowProcW.argtypes = [
            ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM
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
            0, wc.lpszClassName, "MediaControlTrayHandler",
            0, 0, 0, 0, 0, None, None, hInstance, None
        )
        if not hwnd:
            logger.error("Failed to create tray window using CreateWindowExW")
        return hwnd

    def _handle_window_msg(self, hwnd, msg, wparam, lparam):
        try:
            if msg == WM_TRAY:
                if lparam == win32con.WM_LBUTTONDOWN:
                    self._trigger_click_effect(wparam)
                    for ctrl in self.controls:
                        if ctrl["id"] == wparam:
                            # Run action directly
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
            None
        )
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        win32gui.DestroyMenu(hmenu)

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
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, (self.hwnd, ctrl["id"], flags, WM_TRAY, hicon, ctrl["tip"]))
            time.sleep(0.1)

    def _update_tray_icon(self, icon_id, hicon):
        if self.active_hicons.get(icon_id) == hicon:
            return
        self.active_hicons[icon_id] = hicon
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, (self.hwnd, icon_id, win32gui.NIF_ICON, WM_TRAY, hicon, ""))

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
        self.monitor_thread = threading.Thread(target=self.run_monitor_loop, daemon=True)
        self.monitor_thread.start()

    def run_monitor_loop(self):
        # Initialize COM as MTA for this thread to support WinRT calls safely
        hr = ctypes.windll.ole32.CoInitializeEx(None, 2)
        logger.info(f"CoInitializeEx returned {hr}")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
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
                logger.error(f"Failed to request winsdk SessionManager: {e}. Retrying in 5s...")
                await asyncio.sleep(5)

        while True:
            session = None
            info = None
            try:
                session = manager.get_current_session()
                if session:
                    info = session.get_playback_info()
                    status = info.playback_status if info else None

                    if status != self.current_status:
                        self.current_status = status
                        self.update_media_state(status)
                else:
                    if self.current_status is not None:
                        self.current_status = None
                        self.update_media_state(None)
            except Exception as e:
                logger.error(f"Error checking Windows Media session: {e}")
            finally:
                # Force immediate cleanup of winsdk/WinRT COM objects
                if session is not None:
                    del session
                if info is not None:
                    del info
                import gc
                gc.collect()
            await asyncio.sleep(0.5)

    def update_media_state(self, status):
        # Dispatch updates to tray icons (status & dark/light theme checks)
        self.update_play_pause_icon(status)
        self.check_theme_update()

    def run(self):
        user32 = ctypes.windll.user32
        
        # Explicit argtypes/restype for GetMessageW, TranslateMessage, DispatchMessageW
        user32.GetMessageW.restype = ctypes.wintypes.BOOL
        user32.GetMessageW.argtypes = [
            ctypes.POINTER(ctypes.wintypes.MSG), ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.UINT
        ]
        user32.TranslateMessage.restype = ctypes.wintypes.BOOL
        user32.TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]
        user32.DispatchMessageW.restype = ctypes.wintypes.LPARAM
        user32.DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def quit_app(self):
        logger.info("Gracefully quitting Media Control application...")
        self.shutdown()
        # Force exit
        os._exit(0)


if __name__ == "__main__":
    app = MediaControlApp()
    app.run()
