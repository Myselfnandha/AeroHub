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
import time

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing dependencies. Run: pip install pystray Pillow")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.dirname(SCRIPT_DIR)
PS1_PATH = os.path.join(UTILS_DIR, "TouchToggle.ps1")
LOG_PATH = os.path.join(SCRIPT_DIR, "touch_toggle.log")

# ── Logging ──
os.makedirs(SCRIPT_DIR, exist_ok=True)

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
        logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=2*1024*1024, backupCount=2, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("TouchToggle")

# ── State ──
touch_enabled = True
tray_icon = None


def create_icon_image(enabled: bool) -> Image.Image:
    """Draw a tray icon showing touch ON (green) or OFF (red)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    color = (50, 205, 50, 255) if enabled else (255, 0, 0, 255) # LimeGreen / Red
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


def check_touch_state() -> bool:
    """Check if the HID touch screen is currently enabled."""
    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                "Get-PnpDevice -Class 'HIDClass' | Where-Object FriendlyName -match 'touch screen' | Select-Object -ExpandProperty Status"
            ],
            capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW
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
    ]

def show_tooltip(text):
    """Show a custom floating tooltip notification above the taskbar using a separate process."""
    try:
        notifier_script = os.path.join(SCRIPT_DIR, "tooltip_notifier.py")
        subprocess.Popen(
            ["pythonw", notifier_script, text],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        logger.error(f"Failed to spawn tooltip: {e}")

def toggle_touch():
    """Run the PowerShell toggle script elevated in background and poll for completion."""
    global touch_enabled, tray_icon
    logger.info("Toggling touch screen...")

    import ctypes
    
    # Define shell execute constants
    SEE_MASK_NOCLOSEPROCESS = 0x00000040
    SW_HIDE = 0
    WAIT_OBJECT_0 = 0x00000000
    WAIT_TIMEOUT = 0x00000102
    
    # Path to the log file written by PS1
    ps1_log_path = os.path.join(UTILS_DIR, "touch_toggle_run.log")
    
    # Clean previous run log if exists
    if os.path.exists(ps1_log_path):
        try:
            os.remove(ps1_log_path)
        except Exception as e:
            logger.warning(f"Could not remove old PS1 log: {e}")

    try:
        logger.info("Executing PowerShell toggle script (hidden)...")
        # Run powershell via VBS wrapper to guarantee zero window flash
        vbs_path = os.path.join(SCRIPT_DIR, "run_hidden.vbs")
        result = subprocess.run(
            ["wscript.exe", vbs_path, PS1_PATH],
            capture_output=True, text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        exit_code = result.returncode
        if exit_code != 0:
            logger.error(f"PowerShell script failed with exit code {exit_code}")
            logger.error(f"stderr: {result.stderr}")
            logger.error(f"stdout: {result.stdout}")
        else:
            logger.info("PowerShell script completed successfully.")

        # Check and log touch_toggle_run.log contents
        if os.path.exists(ps1_log_path):
            try:
                with open(ps1_log_path, "r", encoding="utf-16le") as f:
                    log_content = f.read()
                logger.info(f"--- PS1 Log Output ---\n{log_content}----------------------")
            except Exception as e1:
                try:
                    with open(ps1_log_path, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    logger.info(f"--- PS1 Log Output (UTF-8 fallback) ---\n{log_content}----------------------")
                except Exception as e2:
                    logger.error(f"Failed to read PS1 log file: {e1} / {e2}")
        else:
            logger.warning("touch_toggle_run.log file not found after PS1 execution.")

        if exit_code != 0:
            logger.error("PowerShell script exited with non-zero status.")

        # Re-check state
        touch_enabled = check_touch_state()
        logger.info(f"Touch screen is now: {'ENABLED' if touch_enabled else 'DISABLED'}")

        # Update icon
        if tray_icon:
            tray_icon.icon = create_icon_image(touch_enabled)
            state_str = "ON" if touch_enabled else "OFF"
            tray_icon.title = f"Touch: {state_str}"
            tray_icon.menu = create_menu()
            
            # Show tooltip notification
            show_tooltip(f"Touch Screen is now {state_str}")

    except Exception as e:
        logger.error(f"Toggle failed: {e}")


def on_toggle(icon, item):
    """Menu callback for toggle action."""
    threading.Thread(target=toggle_touch, daemon=True).start()


def on_quit(icon, item):
    """Quit the tray app."""
    logger.info("Quitting Touch Toggle tray app.")
    icon.stop()


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
        pystray.MenuItem("Quit", on_quit),
    )


def main():
    global touch_enabled, tray_icon

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
    tray_icon.run()


if __name__ == "__main__":
    main()
