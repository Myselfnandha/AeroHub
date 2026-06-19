# ruff: noqa: E402
"""
Touch Toggle — System Tray App
Provides a tray icon that shows touchscreen ON/OFF state.
Left-click toggles the touchscreen by running TouchToggle.ps1 elevated.
"""

import os
import sys
import subprocess
import threading
import logging
import logging.handlers
import json
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import queue

ICON_SUPPORT = False
try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
    ICON_SUPPORT = True
except ImportError:
    pystray = None
    Image = None
    ImageDraw = None
    ImageFont = None

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOGGLES_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(TOGGLES_DIR)
PS1_PATH = os.path.join(SCRIPT_DIR, "TouchToggle.ps1")
LOGS_DIR = os.path.join(PROJECT_DIR, "Logs")
LOG_PATH = os.path.join(LOGS_DIR, "touch_toggle.log")
# Allow importing from parent directory (AeroHub root)
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)
import services.aerohub_core.system_utils as system_utils
try:
    from services.aerohub_core.toast_utils import BaseToast, EmojiPickerPanel
except ImportError:
    pass

# ── Logging ──
os.makedirs(LOGS_DIR, exist_ok=True)

# Set unique AppUserModelID so tray icon appears separately
try:
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.TouchToggle")
except Exception:
    pass
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
logger = logging.getLogger("TouchToggle")

# ── State ──
touch_enabled = True
tray_icon = None


# ── Settings ──
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "touch_settings.json")
DEFAULT_SETTINGS = {
    "toast_pos": "Center",
    "toast_custom_x": 100,
    "toast_custom_y": 100,
    "toast_width": 260,
    "toast_height": 60,
    "toast_bg_color": "#18181b",
    "toast_fg_color": "#ffffff",
    "toast_accent_color": "#ff8800",
    "toast_font_size": 11,
    "toast_font_weight": "bold",
    "toast_font_family": "Segoe UI",
    "toast_emoji": "🖐️",
    "toast_radius": 15,
    "toast_padding_x": 12,
    "toast_padding_y": 10,
    "toast_anim_style": "Slide",
    "toast_opacity": 0.95,
    "toast_border_width": 1,
    "toast_border_color": "#27272a",
    "toast_gradient": False,
    "toast_gradient_end": "#0a0a0a",
    "toast_shadow": True,
    "toast_accent_stripe": False,
    "toast_text_align": "left",
    "toast_auto_dismiss": True,
    "toast_click_action": "dismiss",
    "toast_progress_bar": False,
    "toast_enable_sound": False,
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                saved = json.load(f)
                return {**DEFAULT_SETTINGS, **saved}
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        logger.info("Settings saved.")
    except Exception as e:
        logger.error(f"Error saving settings: {e}")


global_settings = load_settings()

TH = {
    "bg": "#0a0a0a",
    "bg2": "#171717",
    "bg3": "#262626",
    "fg": "#e5e5e5",
    "fg_dim": "#a3a3a3",
    "accent": "#ff8800",
    "border": "#333333",
}


def apply_dwm_rounding(window):
    try:
        import ctypes

        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        value = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(value),
            ctypes.sizeof(value),
        )
    except Exception:
        pass


class SettingsWindow:
    def __init__(self, parent, settings, on_save):
        self.parent = parent
        self.settings = settings
        self.on_save = on_save
        self.entries = {}

    def show(self):
        root = tk.Toplevel(self.parent)
        root.title("Touch Toggle Config")
        root.geometry("600x500")
        root.configure(bg=TH["bg"])
        root.resizable(False, False)
        root.grab_set()

        try:
            apply_dwm_rounding(root)
        except Exception:
            pass

        try:
            from PIL import ImageTk
            icon_img = create_icon_image(touch_enabled)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, self.icon_photo)
        except Exception as e:
            logger.error(f"Failed to set window icon: {e}")

        def on_closing():
            if (
                hasattr(self, "preview_instance")
                and self.preview_instance
                and hasattr(self.preview_instance, "force_close")
            ):
                self.preview_instance.force_close()
            root.grab_release()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=180)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="TOUCH.SYS",
            font=("Consolas", 16, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.btn_save = tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["bg3"],
            fg=TH["accent"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, pady=20, padx=20, fill=tk.X)

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20
        )

        canvas = tk.Canvas(self.content_area, bg=TH["bg"], highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                w = event.widget.winfo_containing(event.x_root, event.y_root)
                while w:
                    if isinstance(w, tk.Canvas):
                        w.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        break
                    w = w.master
            except Exception:
                pass

        self.content_area.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            scrollable_frame,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        f2_right = tk.Frame(f_top, bg=TH["bg"])
        f2_right.pack(side=tk.LEFT, fill=tk.Y)

        positions = [
            "Top-Left",
            "Top-Center",
            "Top-Right",
            "Bottom-Left",
            "Bottom-Center",
            "Bottom-Right",
            "Middle-Left",
            "Middle-Right",
            "Custom",
        ]
        animations = ["Slide", "Fade", "Bounce", "Scale", "Typewriter", "Glow", "Drop"]
        fonts = ["Segoe UI", "Consolas", "Cascadia Code", "Arial", "Verdana"]
        actions = ["dismiss", "snooze", "settings"]

        self._add_combo(f2_left, "Position:", "toast_pos", 0, positions)
        self._add_combo(f2_left, "Animation:", "toast_anim_style", 1, animations)
        self._add_field(f2_left, "Width (px):", "toast_width", 2)
        self._add_field(f2_left, "Height (px):", "toast_height", 3)
        self._add_color_field(f2_left, "Background:", "toast_bg_color", 4)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 5)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 6)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 7, ["normal", "bold"]
        )
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 8, fonts)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 9)
        self._add_field(f2_left, "Custom X:", "toast_custom_x", 10)
        self._add_field(f2_left, "Custom Y:", "toast_custom_y", 11)

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X:", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y:", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity:", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width:", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End:", "toast_gradient_end", 7)
        self._add_combo(
            f2_right, "Text Align:", "toast_text_align", 8, ["left", "center", "right"]
        )
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 9, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration_sec", 10)
        self._add_field(f2_right, "Transition (ms):", "toast_transition_time_ms", 11)

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))
        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)

        btn_frame = tk.Frame(scrollable_frame, bg=TH["bg"])
        btn_frame.pack(fill=tk.X, pady=20)

        tk.Button(
            btn_frame,
            text="[ PREVIEW_UI ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
            activebackground=TH["bg3"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._preview_toast,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))
        tk.Entry(
            parent_frame,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=10,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, values[0]))
        ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=8,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame, text=label, font=("Consolas", 9), bg=TH["bg"], fg=TH["fg_dim"]
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=self.settings.get(key, "#ffffff"))

        def choose_color(v=var):
            color_code = colorchooser.askcolor(
                title="Choose color", initialcolor=v.get()
            )[1]
            if color_code:
                v.set(color_code)
                btn.config(bg=color_code)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=6,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(10, 0))
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_grid_chk(self, parent_frame, label, key, row):
        var = tk.BooleanVar(value=self.settings.get(key, True))
        tk.Checkbutton(
            parent_frame,
            text=label.upper(),
            variable=var,
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            selectcolor=TH["bg2"],
            activebackground=TH["bg"],
            activeforeground=TH["accent"],
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=8)
        self.entries[key] = (var, "bool")
        var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_emoji_picker(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "🖐️")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.parent, _on_select)

        btn = tk.Button(
            f,
            text="Pick",
            font=("Consolas", 8),
            bg=TH["bg2"],
            fg=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            command=_open_picker,
        )
        btn.pack(side=tk.LEFT)
        self.entries[key] = (var, True)

    def _schedule_preview(self):
        self._preview_toast(is_auto_edit=True)

    def _preview_toast(self, is_auto_edit=False):
        toast_exists = False
        if hasattr(self, "preview_instance") and self.preview_instance:
            if getattr(self.preview_instance, "toast_window", None) and self.preview_instance.toast_window.winfo_exists():
                toast_exists = True
            else:
                self.preview_instance = None

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif not var_type:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False

        if toast_exists:
            try:
                self.preview_instance.update_settings(temp_settings)
            except Exception as e:
                logger.error(f"Error updating preview in-place: {e}")
        else:
            if hasattr(self, "preview_instance") and self.preview_instance:
                try:
                    self.preview_instance.force_close()
                except Exception:
                    pass
            self.preview_instance = BaseToast(
                self.parent, "TOUCH PREVIEW", "Preview Toast", temp_settings
            )
            self.preview_instance.show()

    def _save_settings_clicked(self):
        if hasattr(self, "preview_instance") and self.preview_instance:
            try:
                self.preview_instance.force_close()
            except Exception:
                pass
            self.preview_instance = None

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif not var_type:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        save_settings(self.settings)
        self.on_save(self.settings)

        self.btn_save.config(text="[ SAVED ]", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="[ SAVE_CFG ]", state=tk.NORMAL)
            except Exception:
                pass
        self.parent.after(2000, reset_btn)


def create_icon_image(enabled: bool) -> Image.Image:
    """Draw a tray icon showing touch ON (green) or OFF (red)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    color = (50, 205, 50, 255) if enabled else (255, 0, 0, 255)  # LimeGreen / Red
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)

    # Draw "T" for Touch
    try:
        font = ImageFont.truetype("arialbd.ttf", 36)
    except IOError:
        font = ImageFont.load_default()

    text = "T"
    # Get bounding box to center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Adjust for visual center
    x = (size - text_w) / 2
    y = (size - text_h) / 2 - 4

    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    return img


gui_queue = queue.Queue()
tk_root = None


def _process_gui_queue_loop():
    while not gui_queue.empty():
        try:
            action = gui_queue.get_nowait()
            if action == "settings":

                def on_saved(new_settings):
                    global global_settings
                    global_settings = new_settings

                SettingsWindow(tk_root, dict(global_settings), on_saved).show()
            elif isinstance(action, dict) and action.get("type") == "toast":
                temp_settings = dict(global_settings)
                state = action.get("state", "on")
                if state == "off":
                    temp_settings["toast_accent_color"] = "#ff3b30"
                    temp_settings["toast_emoji"] = "🚫"
                else:
                    temp_settings["toast_accent_color"] = "#34c759"
                    temp_settings["toast_emoji"] = "🖐️"
                BaseToast(tk_root, action["title"], action["msg"], temp_settings).show()
        except Exception as e:
            logger.error(f"Error processing GUI queue: {e}")
    tk_root.after(100, _process_gui_queue_loop)


def open_settings(icon, item):
    gui_queue.put("settings")


def check_touch_state() -> bool:
    """Check if the HID touch screen is currently enabled."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                (
                    "Get-PnpDevice -Class 'HIDClass' | Where-Object FriendlyName -match 'touch screen' "
                    "| Select-Object -ExpandProperty Status"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        status = result.stdout.strip().lower()
        logger.info(f"Touch screen status query result: '{status}'")
        return status == "ok"
    except Exception as e:
        logger.error(f"Failed to check touch state: {e}")
        return True  # Assume enabled on error


class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("fMask", ctypes.c_ulong),
        ("hwnd", ctypes.c_void_p),
        ("lpVerb", ctypes.c_wchar_p),
        ("lpFile", ctypes.c_wchar_p),
        ("lpParameters", ctypes.c_wchar_p),
        ("lpDirectory", ctypes.c_wchar_p),
        ("nShow", ctypes.c_int),
        ("hInstApp", ctypes.c_void_p),
        ("lpIDList", ctypes.c_void_p),
        ("lpClass", ctypes.c_wchar_p),
        ("hkeyClass", ctypes.c_void_p),
        ("dwHotKey", ctypes.c_ulong),
        ("hIconOrMonitor", ctypes.c_void_p),
        ("hProcess", ctypes.c_void_p),
    ]


def show_tooltip(text, state):
    """Show a custom floating tooltip notification via gui_queue and BaseToast."""
    gui_queue.put(
        {"type": "toast", "title": "Touch Screen", "msg": text, "state": state}
    )


def toggle_touch():
    """Run the PowerShell toggle script elevated via ShellExecuteExW (runas)."""
    global touch_enabled
    logger.info("Toggling touch screen...")

    # Path to the log file written by PS1
    ps1_log_path = os.path.join(LOGS_DIR, "touch_toggle_run.log")

    # Clean previous run log if exists
    if os.path.exists(ps1_log_path):
        try:
            os.remove(ps1_log_path)
        except Exception as e:
            logger.warning(f"Could not remove old PS1 log: {e}")

    try:
        if not os.path.exists(PS1_PATH):
            logger.error(f"PowerShell script not found: {PS1_PATH}")
            return

        is_admin = False
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            pass

        if is_admin:
            logger.info(
                f"Already running as admin. Executing PowerShell script directly: {PS1_PATH}"
            )
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-WindowStyle",
                    "Hidden",
                    "-File",
                    PS1_PATH,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            logger.info("Direct PowerShell script execution completed.")
        else:
            logger.info(
                f"Not running as admin. Executing elevated PowerShell script via ShellExecuteExW: {PS1_PATH}"
            )

            # Use ShellExecuteExW with 'runas' verb for proper UAC elevation
            params = f'-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{PS1_PATH}"'

            sei = SHELLEXECUTEINFO()
            sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
            sei.fMask = 0x00000040  # SEE_MASK_NOCLOSEPROCESS
            sei.hwnd = None
            sei.lpVerb = "runas"
            sei.lpFile = "powershell.exe"
            sei.lpParameters = params
            sei.lpDirectory = None
            sei.nShow = 0  # SW_HIDE

            if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
                error_code = ctypes.GetLastError()
                logger.error(f"ShellExecuteExW failed with error code: {error_code}")
                return

            # Wait for the elevated process to finish using hProcess handle
            if sei.hProcess:
                logger.info("Waiting for elevated PowerShell process to complete...")
                INFINITE = 0xFFFFFFFF
                ctypes.windll.kernel32.WaitForSingleObject(
                    ctypes.c_void_p(sei.hProcess), INFINITE
                )
                ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(sei.hProcess))
            else:
                # Fallback: wait a bit for the script to run
                import time

                time.sleep(3)

            logger.info("Elevated PowerShell script execution completed.")

        # Check and log touch_toggle_run.log contents
        if os.path.exists(ps1_log_path):
            try:
                with open(ps1_log_path, "r", encoding="utf-16le") as f:
                    log_content = f.read()
                logger.info(
                    f"--- PS1 Log Output ---\n{log_content}----------------------"
                )
            except Exception as e1:
                try:
                    with open(ps1_log_path, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    logger.info(
                        f"--- PS1 Log Output (UTF-8 fallback) ---\n{log_content}----------------------"
                    )
                except Exception as e2:
                    logger.error(f"Failed to read PS1 log file: {e1} / {e2}")
        else:
            logger.warning(f"touch_toggle_run.log not found at: {ps1_log_path}")

        # Re-check state
        touch_enabled = check_touch_state()
        logger.info(
            f"Touch screen is now: {'ENABLED' if touch_enabled else 'DISABLED'}"
        )

        # Update icon
        if tray_icon:
            tray_icon.icon = create_icon_image(touch_enabled)
            state_str = "ON" if touch_enabled else "OFF"
            tray_icon.title = f"Touch: {state_str}"
            tray_icon.menu = create_menu()

            # Show tooltip notification
            show_tooltip(
                f"Touch Screen is now {state_str}", "on" if touch_enabled else "off"
            )

    except Exception as e:
        logger.error(f"Toggle failed: {e}")


def on_toggle(icon, item):
    """Menu callback for toggle action."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def on_quit(icon, item):
    """Quit the tray app."""
    logger.info("Quitting Touch Toggle tray app.")
    icon.stop()
    if tk_root:
        tk_root.quit()


def on_click(icon, item):
    """Left-click handler — toggle touchscreen."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def create_menu():
    """Create the tray context menu."""
    state_text = f"Touch: {'ON ✓' if touch_enabled else 'OFF ✗'}"
    return pystray.Menu(
        pystray.MenuItem(state_text, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Toggle Touch Screen", on_toggle, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings", open_settings),
        pystray.MenuItem("Quit", on_quit),
    )


def main():
    global touch_enabled, tray_icon

    if not ICON_SUPPORT:
        logger.error(
            "TouchToggle requires pystray and Pillow. Install dependencies from requirements.txt and retry."
        )
        sys.exit(1)

    logger.info("=" * 50)
    logger.info("Touch Toggle Tray App starting...")

    # Check initial state
    touch_enabled = check_touch_state()
    logger.info(f"Initial touch state: {'ENABLED' if touch_enabled else 'DISABLED'}")

    # Create tray icon
    icon_image = create_icon_image(touch_enabled)
    tray_icon = pystray.Icon(
        name="TouchToggle",
        icon=icon_image,
        title=f"Touch: {'ON' if touch_enabled else 'OFF'}",
        menu=create_menu(),
    )

    logger.info("Tray icon created. Running...")

    global tk_root
    tk_root = tk.Tk()
    tk_root.withdraw()

    icon_thread = threading.Thread(target=tray_icon.run, daemon=True)
    icon_thread.start()

    # Start parent process monitoring
    system_utils.monitor_parent_process(lambda: on_quit(tray_icon, None))

    tk_root.after(100, _process_gui_queue_loop)
    tk_root.mainloop()


if __name__ == "__main__":
    main()
