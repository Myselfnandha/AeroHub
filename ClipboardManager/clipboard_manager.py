"""
Clipboard Manager — Background clipboard history tracker with desktop GUI.
Tracks text and file-path clipboard entries, stores in SQLite, provides
search/browse/re-copy UI. Auto-exports to Markdown when entries exceed 1000.
"""

import os
import sys
import time
import sqlite3
import ctypes
import ctypes.wintypes
import threading
import logging
import logging.handlers
import datetime
import hashlib
import tkinter as tk
from tkinter import messagebox

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Missing deps. Run: pip install pystray Pillow")
    sys.exit(1)

try:
    import win32clipboard
    import win32con
except ImportError:
    print("Missing deps. Run: pip install pywin32")
    sys.exit(1)

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "clipboard_history.db")
EXPORT_DIR = os.path.join(SCRIPT_DIR, "exports")
LOGS_DIR = r"c:\Users\NANDHA A\Desktop\UTILITIES\Logs"
LOG_PATH = os.path.join(LOGS_DIR, "clipboard_manager.log")

os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Set unique AppUserModelID so the tray icon appears separately (not grouped with other Python processes)
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AeroHub.ClipboardManager")
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
logger = logging.getLogger("ClipboardManager")

# ── Theme ──
THEME = {
    "bg": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_entry": "#0f3460",
    "fg": "#e0e0e0",
    "fg_dim": "#8892b0",
    "accent": "#00d4ff",
    "accent_hover": "#00b4d8",
    "danger": "#ff3366",
    "success": "#00ff88",
    "border": "#2d2d5e",
    "selected": "#0f3460",
}

# ── Default Config & Constants ──
DEFAULT_CONFIG = {
    "max_entries": 1000,
    "export_batch": 500,
    "auto_export": True
}
CF_HDROP = 15  # clipboard format for file lists
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

def load_config() -> dict:
    import json
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                # Ensure all default keys exist
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
        except Exception as e:
            logger.error(f"Failed to load config.json: {e}")
    return dict(DEFAULT_CONFIG)

def save_config(cfg: dict):
    import json
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save config.json: {e}")


# ══════════════════════════════════════════════════════════
#  Database
# ══════════════════════════════════════════════════════════
class ClipboardDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        with self.lock:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS clipboard_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON clipboard_history(timestamp DESC)
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hash ON clipboard_history(content_hash)
            """)
            self.conn.commit()

    def add_entry(self, content_type: str, content: str) -> bool:
        """Add entry if not a duplicate of the most recent one. Returns True if added."""
        content_hash = hashlib.md5(content.encode("utf-8", errors="replace")).hexdigest()
        with self.lock:
            # Check if identical to last entry
            row = self.conn.execute(
                "SELECT content_hash FROM clipboard_history ORDER BY id DESC LIMIT 1"
            ).fetchone()
            if row and row[0] == content_hash:
                return False  # Duplicate of last entry

            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conn.execute(
                "INSERT INTO clipboard_history (content_type, content, content_hash, timestamp) VALUES (?, ?, ?, ?)",
                (content_type, content, content_hash, ts),
            )
            self.conn.commit()
            return True

    def get_entries(self, search: str = "", limit: int = 500) -> list:
        """Return entries newest first. Optional search filter."""
        with self.lock:
            if search:
                query = "SELECT id, content_type, content, timestamp FROM clipboard_history WHERE content LIKE ? ORDER BY id DESC LIMIT ?"
                return self.conn.execute(query, (f"%{search}%", limit)).fetchall()
            else:
                query = "SELECT id, content_type, content, timestamp FROM clipboard_history ORDER BY id DESC LIMIT ?"
                return self.conn.execute(query, (limit,)).fetchall()

    def get_count(self) -> int:
        with self.lock:
            return self.conn.execute("SELECT COUNT(*) FROM clipboard_history").fetchone()[0]

    def delete_entry(self, entry_id: int):
        with self.lock:
            self.conn.execute("DELETE FROM clipboard_history WHERE id = ?", (entry_id,))
            self.conn.commit()

    def clear_all(self):
        with self.lock:
            self.conn.execute("DELETE FROM clipboard_history")
            self.conn.commit()

    def get_oldest_entries(self, count: int) -> list:
        with self.lock:
            return self.conn.execute(
                "SELECT id, content_type, content, timestamp FROM clipboard_history ORDER BY id ASC LIMIT ?",
                (count,),
            ).fetchall()

    def delete_ids(self, ids: list):
        with self.lock:
            placeholders = ",".join("?" * len(ids))
            self.conn.execute(f"DELETE FROM clipboard_history WHERE id IN ({placeholders})", ids)
            self.conn.commit()

    def close(self):
        self.conn.close()


# ══════════════════════════════════════════════════════════
#  Clipboard Listener (Win32 message loop)
# ══════════════════════════════════════════════════════════
class ClipboardListener:
    """Listens for clipboard changes via WM_CLIPBOARDUPDATE."""

    WM_CLIPBOARDUPDATE = 0x031D

    def __init__(self, callback):
        self.callback = callback
        self._hwnd = None
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        """Create an invisible window and listen for clipboard updates."""
        try:
            # Manually define WNDCLASSW and WNDPROC types for 64-bit safety
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

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            # Declare function signatures for 64-bit safety
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

            user32.AddClipboardFormatListener.restype = ctypes.wintypes.BOOL
            user32.AddClipboardFormatListener.argtypes = [ctypes.wintypes.HWND]

            user32.DefWindowProcW.restype = ctypes.wintypes.LPARAM
            user32.DefWindowProcW.argtypes = [
                ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM
            ]

            user32.PostQuitMessage.restype = None
            user32.PostQuitMessage.argtypes = [ctypes.c_int]

            user32.GetMessageW.restype = ctypes.wintypes.BOOL
            user32.GetMessageW.argtypes = [
                ctypes.POINTER(ctypes.wintypes.MSG), ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.UINT
            ]

            user32.TranslateMessage.restype = ctypes.wintypes.BOOL
            user32.TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

            user32.DispatchMessageW.restype = ctypes.wintypes.LPARAM
            user32.DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

            def wnd_proc(hwnd, msg, wparam, lparam):
                if msg == self.WM_CLIPBOARDUPDATE:
                    try:
                        self._on_clipboard_change()
                    except Exception as e:
                        logger.error(f"Clipboard change handler error: {e}")
                    return 0
                elif msg == win32con.WM_DESTROY:
                    user32.PostQuitMessage(0)
                    return 0
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

            self._wnd_proc = WNDPROC(wnd_proc)  # prevent GC

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
            wc.lpszClassName = "ClipboardManagerListener"

            user32.RegisterClassW(ctypes.byref(wc))

            self._hwnd = user32.CreateWindowExW(
                0, wc.lpszClassName, "ClipboardManagerHidden",
                0, 0, 0, 0, 0, None, None, hInstance, None
            )

            if not self._hwnd:
                logger.error("Failed to create clipboard listener window.")
                return

            if user32.AddClipboardFormatListener(self._hwnd):
                logger.info("Clipboard listener registered successfully.")
            else:
                logger.error("Failed to register clipboard format listener.")

            # Win32 message loop
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception as e:
            logger.exception(f"Unhandled exception in clipboard listener thread: {e}")

    def _on_clipboard_change(self):
        """Read clipboard content and invoke callback."""
        time.sleep(0.05)  # Small delay for clipboard to settle
        try:
            win32clipboard.OpenClipboard()
            try:
                # Try text first
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                    if data and data.strip():
                        self.callback("text", data.strip())
                        return

                # Try file drop list
                if win32clipboard.IsClipboardFormatAvailable(CF_HDROP):
                    data = win32clipboard.GetClipboardData(CF_HDROP)
                    if data:
                        # data is a tuple of file paths
                        file_paths = "\n".join(data) if isinstance(data, (list, tuple)) else str(data)
                        self.callback("filepath", file_paths)
                        return
            finally:
                win32clipboard.CloseClipboard()
        except Exception as e:
            # Clipboard may be locked by another app
            logger.debug(f"Could not read clipboard: {e}")


# ══════════════════════════════════════════════════════════
#  Auto-Export
# ══════════════════════════════════════════════════════════
def export_to_markdown(db: ClipboardDB, config: dict):
    """Export oldest entries to markdown and delete them based on config."""
    if not config.get("auto_export", True):
        return

    count = db.get_count()
    max_entries = config.get("max_entries", 1000)
    export_batch = config.get("export_batch", 500)

    if count <= max_entries:
        return

    entries = db.get_oldest_entries(export_batch)
    if not entries:
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = os.path.join(EXPORT_DIR, f"clipboard_export_{ts}.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Clipboard History Export\n")
        f.write(f"**Exported:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Entries:** {len(entries)}\n\n---\n\n")

        for entry_id, content_type, content, timestamp in entries:
            f.write(f"## [{timestamp}] — {content_type.upper()}\n\n")
            f.write(f"```\n{content}\n```\n\n---\n\n")

    ids = [e[0] for e in entries]
    db.delete_ids(ids)
    logger.info(f"Auto-exported {len(entries)} entries to {md_path}")


# ══════════════════════════════════════════════════════════
#  GUI — Clipboard Manager Window
# ══════════════════════════════════════════════════════════
class ClipboardManagerGUI:
    def __init__(self, db: ClipboardDB):
        self.db = db
        self.root = None
        self._visible = False

    def show(self):
        """Show or create the manager window."""
        if self.root:
            try:
                if isinstance(self.root, tk.Toplevel):
                    self.root.deiconify()
                    self.root.lift()
                    self.root.focus_force()
                    self._visible = True
                    self.refresh_list()
                    return
            except tk.TclError:
                pass

        self._create_window()

    def hide(self):
        if self.root:
            try:
                self.root.withdraw()
                self._visible = False
            except tk.TclError:
                pass

    def _create_window(self):
        self.root = tk.Toplevel() if hasattr(self, '_tk_root') else tk.Tk()
        self.root.title("Clipboard Manager")
        self.root.geometry("900x600")
        self.root.configure(bg=THEME["bg"])
        self.root.minsize(700, 400)
        self._visible = True

        # Window icon
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        # ── Header ──
        header = tk.Frame(self.root, bg=THEME["bg"], pady=10, padx=15)
        header.pack(fill=tk.X)

        tk.Label(
            header, text="📋 Clipboard Manager", font=("Segoe UI", 16, "bold"),
            bg=THEME["bg"], fg=THEME["accent"]
        ).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="")
        tk.Label(
            header, textvariable=self.status_var, font=("Segoe UI", 10),
            bg=THEME["bg"], fg=THEME["fg_dim"]
        ).pack(side=tk.RIGHT)

        # ── Search Bar ──
        search_frame = tk.Frame(self.root, bg=THEME["bg"], padx=15)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            search_frame, text="🔍", font=("Segoe UI", 14),
            bg=THEME["bg"], fg=THEME["fg_dim"]
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_list())
        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("Segoe UI", 12), bg=THEME["bg_entry"], fg=THEME["fg"],
            insertbackground=THEME["accent"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=THEME["accent"],
            highlightbackground=THEME["border"]
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        # Clear search
        clear_btn = tk.Button(
            search_frame, text="✕", font=("Segoe UI", 10),
            bg=THEME["bg_secondary"], fg=THEME["fg_dim"],
            relief=tk.FLAT, cursor="hand2",
            command=lambda: self.search_var.set("")
        )
        clear_btn.pack(side=tk.LEFT, padx=(8, 0))

        # ── Content Area (Split: list + preview) ──
        content = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL, bg=THEME["border"],
            sashwidth=3, sashrelief=tk.FLAT
        )
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        # ── List Frame ──
        list_frame = tk.Frame(content, bg=THEME["bg_secondary"])
        content.add(list_frame, width=450)

        # Listbox with scrollbar
        list_container = tk.Frame(list_frame, bg=THEME["bg_secondary"])
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_container,
            font=("Consolas", 10),
            bg=THEME["bg_secondary"], fg=THEME["fg"],
            selectbackground=THEME["selected"],
            selectforeground=THEME["accent"],
            relief=tk.FLAT, borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle="none",
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        self.listbox.bind("<Double-1>", self._on_double_click)
        self.listbox.bind("<Button-3>", self._on_right_click)

        # ── Preview Frame ──
        preview_frame = tk.Frame(content, bg=THEME["bg"])
        content.add(preview_frame, width=400)

        tk.Label(
            preview_frame, text="Preview", font=("Segoe UI", 11, "bold"),
            bg=THEME["bg"], fg=THEME["fg_dim"], anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(10, 5))

        self.preview_text = tk.Text(
            preview_frame,
            font=("Consolas", 10),
            bg=THEME["bg_entry"], fg=THEME["fg"],
            relief=tk.FLAT, wrap=tk.WORD,
            highlightthickness=1, highlightcolor=THEME["accent"],
            highlightbackground=THEME["border"],
            insertbackground=THEME["accent"],
            state=tk.DISABLED,
            padx=10, pady=10,
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # ── Bottom Bar ──
        bottom = tk.Frame(self.root, bg=THEME["bg"], padx=15, pady=8)
        bottom.pack(fill=tk.X)

        btn_style = {"font": ("Segoe UI", 9), "relief": tk.FLAT, "cursor": "hand2", "padx": 12, "pady": 4}

        tk.Button(
            bottom, text="🗑 Clear All", bg=THEME["danger"], fg="#fff",
            command=self._clear_all, **btn_style
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            bottom, text="📄 Export to MD", bg=THEME["accent"], fg="#000",
            command=self._manual_export, **btn_style
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            bottom, text="🔄 Refresh", bg=THEME["bg_secondary"], fg=THEME["fg"],
            command=self.refresh_list, **btn_style
        ).pack(side=tk.LEFT)

        tk.Button(
            bottom, text="⚙️ Settings", bg=THEME["bg_secondary"], fg=THEME["fg"],
            command=self.open_settings, **btn_style
        ).pack(side=tk.LEFT, padx=(8, 0))

        self.count_var = tk.StringVar()
        tk.Label(
            bottom, textvariable=self.count_var, font=("Segoe UI", 9),
            bg=THEME["bg"], fg=THEME["fg_dim"]
        ).pack(side=tk.RIGHT)

        # ── Populate ──
        self.entries_cache = []
        self.refresh_list()

    def open_settings(self):
        """Open a settings window to edit config.json."""
        settings_win = tk.Toplevel(self.root if self.root else None)
        settings_win.title("Clipboard Settings")
        settings_win.geometry("360x280")
        settings_win.configure(bg=THEME["bg"])
        settings_win.resizable(False, False)
        settings_win.grab_set()

        if self.root:
            settings_win.transient(self.root)

        # Apply rounded corners
        settings_win.update_idletasks()
        try:
            hwnd = settings_win.winfo_id()
            import ctypes
            dwmapi = ctypes.windll.dwmapi
            corner_pref = ctypes.c_int(2)
            dwmapi.DwmSetWindowAttribute(
                ctypes.c_void_p(hwnd),
                33,
                ctypes.byref(corner_pref),
                ctypes.sizeof(corner_pref)
            )
        except Exception:
            pass

        tk.Label(
            settings_win, text="⚙️ Clipboard Settings", font=("Segoe UI", 12, "bold"),
            bg=THEME["bg"], fg=THEME["accent"]
        ).pack(pady=15)

        config = self.app.config

        max_frame = tk.Frame(settings_win, bg=THEME["bg"])
        max_frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(max_frame, text="Max Entries:", font=("Segoe UI", 10), bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        max_entry_var = tk.StringVar(value=str(config["max_entries"]))
        max_input = tk.Entry(
            max_frame, textvariable=max_entry_var, width=10, font=("Segoe UI", 10),
            bg=THEME["bg_entry"], fg=THEME["fg"], relief=tk.FLAT, insertbackground=THEME["accent"],
            highlightthickness=1, highlightcolor=THEME["accent"], highlightbackground=THEME["border"]
        )
        max_input.pack(side=tk.RIGHT)

        batch_frame = tk.Frame(settings_win, bg=THEME["bg"])
        batch_frame.pack(fill=tk.X, padx=30, pady=5)
        tk.Label(batch_frame, text="Export Batch Size:", font=("Segoe UI", 10), bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        batch_entry_var = tk.StringVar(value=str(config["export_batch"]))
        batch_input = tk.Entry(
            batch_frame, textvariable=batch_entry_var, width=10, font=("Segoe UI", 10),
            bg=THEME["bg_entry"], fg=THEME["fg"], relief=tk.FLAT, insertbackground=THEME["accent"],
            highlightthickness=1, highlightcolor=THEME["accent"], highlightbackground=THEME["border"]
        )
        batch_input.pack(side=tk.RIGHT)

        auto_frame = tk.Frame(settings_win, bg=THEME["bg"])
        auto_frame.pack(fill=tk.X, padx=30, pady=10)
        auto_var = tk.BooleanVar(value=config["auto_export"])
        auto_cb = tk.Checkbutton(
            auto_frame, text="Enable Auto-Export to Markdown", variable=auto_var, font=("Segoe UI", 10),
            bg=THEME["bg"], fg=THEME["fg"], selectcolor=THEME["bg_secondary"],
            activebackground=THEME["bg"], activeforeground=THEME["fg"],
            cursor="hand2"
        )
        auto_cb.pack(side=tk.LEFT)

        def save_and_close():
            try:
                me = int(max_entry_var.get())
                eb = int(batch_entry_var.get())
                if me <= 0 or eb <= 0:
                    raise ValueError("Values must be positive integers.")
                config["max_entries"] = me
                config["export_batch"] = eb
                config["auto_export"] = auto_var.get()
                save_config(config)
                settings_win.destroy()
                self.status_var.set("✓ Settings saved!")
            except Exception as e:
                messagebox.showerror("Invalid Input", f"Please enter valid positive integers.\n{e}", parent=settings_win)

        btn_frame = tk.Frame(settings_win, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, padx=30, pady=20)
        
        btn_style = {"font": ("Segoe UI", 9), "relief": tk.FLAT, "cursor": "hand2", "padx": 15, "pady": 4}
        
        tk.Button(btn_frame, text="Save Settings", bg=THEME["accent"], fg="#000", command=save_and_close, **btn_style).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Cancel", bg=THEME["bg_secondary"], fg=THEME["fg"], command=settings_win.destroy, **btn_style).pack(side=tk.RIGHT)

    def refresh_list(self):
        """Reload entries from DB into the listbox."""
        if not self.root:
            return
        try:
            search = self.search_var.get().strip()
            self.entries_cache = self.db.get_entries(search=search, limit=500)

            self.listbox.delete(0, tk.END)
            for entry_id, content_type, content, timestamp in self.entries_cache:
                # Truncate for display
                preview = content.replace("\n", " ").replace("\r", "")[:80]
                icon = "📝" if content_type == "text" else "📁"
                ts_short = timestamp[5:]  # strip year
                self.listbox.insert(tk.END, f" {icon} [{ts_short}]  {preview}")

            total = self.db.get_count()
            self.count_var.set(f"Total: {total} entries")
            self.status_var.set(f"Showing {len(self.entries_cache)} of {total}")
        except Exception as e:
            logger.error(f"Refresh error: {e}")

    def _on_select(self, event):
        """Show full content in preview pane."""
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.entries_cache):
            return
        _, content_type, content, timestamp = self.entries_cache[idx]

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", f"[{timestamp}] — {content_type.upper()}\n\n{content}")
        self.preview_text.config(state=tk.DISABLED)

    def _on_double_click(self, event):
        """Re-copy selected entry to clipboard."""
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.entries_cache):
            return
        _, content_type, content, _ = self.entries_cache[idx]

        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(content, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            self.status_var.set("✓ Copied to clipboard!")
            logger.info(f"Re-copied entry to clipboard (type={content_type})")
        except Exception as e:
            logger.error(f"Failed to copy: {e}")
            self.status_var.set(f"✗ Copy failed: {e}")

    def _on_right_click(self, event):
        """Show context menu."""
        sel = self.listbox.curselection()
        if not sel:
            return

        menu = tk.Menu(self.root, tearoff=0, bg=THEME["bg_secondary"], fg=THEME["fg"],
                       activebackground=THEME["accent"], activeforeground="#000",
                       font=("Segoe UI", 10))
        menu.add_command(label="📋 Copy", command=lambda: self._on_double_click(None))
        menu.add_command(label="🗑 Delete", command=self._delete_selected)
        menu.add_separator()
        menu.add_command(label="📄 Export Selected", command=self._export_selected)
        menu.post(event.x_root, event.y_root)

    def _delete_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.entries_cache):
            return
        entry_id = self.entries_cache[idx][0]
        self.db.delete_entry(entry_id)
        self.refresh_list()

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all clipboard history?", parent=self.root):
            self.db.clear_all()
            self.refresh_list()
            self.status_var.set("✓ History cleared")

    def _manual_export(self):
        """Manual export all entries to markdown."""
        entries = self.db.get_entries(limit=10000)
        if not entries:
            self.status_var.set("Nothing to export")
            return

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        md_path = os.path.join(EXPORT_DIR, f"clipboard_export_{ts}.md")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Clipboard History Export\n")
            f.write(f"**Exported:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Entries:** {len(entries)}\n\n---\n\n")
            for entry_id, content_type, content, timestamp in entries:
                f.write(f"## [{timestamp}] — {content_type.upper()}\n\n```\n{content}\n```\n\n---\n\n")

        self.status_var.set(f"✓ Exported {len(entries)} entries")
        logger.info(f"Manual export: {len(entries)} entries to {md_path}")

    def _export_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.entries_cache):
            return
        _, content_type, content, timestamp = self.entries_cache[idx]

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        md_path = os.path.join(EXPORT_DIR, f"clipboard_single_{ts}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Clipboard Entry\n\n**Time:** {timestamp}\n**Type:** {content_type}\n\n```\n{content}\n```\n")
        self.status_var.set("✓ Entry exported")


# ══════════════════════════════════════════════════════════
#  Tray Icon
# ══════════════════════════════════════════════════════════
def create_tray_icon_image() -> Image.Image:
    """Create a clipboard-themed tray icon."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Clipboard board
    draw.rounded_rectangle([12, 4, 52, 58], radius=4, fill=(0, 212, 255, 230))
    # Clip at top
    draw.rounded_rectangle([22, 0, 42, 12], radius=3, fill=(0, 180, 220, 255))
    # Paper lines
    for y in [20, 28, 36, 44]:
        draw.line([20, y, 44, y], fill=(26, 26, 46, 200), width=2)

    return img


# ══════════════════════════════════════════════════════════
#  Main Application
# ══════════════════════════════════════════════════════════
class ClipboardManagerApp:
    def __init__(self):
        self.config = load_config()
        self.db = ClipboardDB(DB_PATH)
        self.gui = ClipboardManagerGUI(self.db)
        self.gui.app = self
        self.listener = ClipboardListener(self._on_clipboard_change)
        self.tray_icon = None
        self._running = True

    def _on_clipboard_change(self, content_type: str, content: str):
        """Called when clipboard content changes."""
        added = self.db.add_entry(content_type, content)
        if added:
            logger.info(f"New clipboard entry: {content_type} ({len(content)} chars)")
            # Auto-export check
            export_to_markdown(self.db, self.config)
            # Refresh GUI if visible
            if self.gui._visible and self.gui.root:
                try:
                    self.gui.root.after(100, self.gui.refresh_list)
                except Exception:
                    pass

    def _on_open(self, icon, item):
        """Open the manager window."""
        if self.gui.root:
            self.gui.root.after(0, self.gui.show)
        else:
            self.gui.show()

    def _on_settings(self, icon, item):
        """Open settings dialog."""
        if self.gui.root:
            self.gui.root.after(0, lambda: [self.gui.show(), self.gui.open_settings()])
        else:
            self.gui.show()
            self.gui.root.after(100, self.gui.open_settings)

    def _on_clear(self, icon, item):
        self.db.clear_all()
        logger.info("Clipboard history cleared via tray menu.")

    def _on_export(self, icon, item):
        export_to_markdown(self.db, self.config)

    def _on_quit(self, icon, item):
        logger.info("Shutting down Clipboard Manager...")
        self._running = False
        icon.stop()
        self.db.close()
        os._exit(0)

    def run(self):
        logger.info("=" * 50)
        logger.info("Clipboard Manager starting...")
        logger.info(f"Database: {DB_PATH}")
        logger.info(f"Current entries: {self.db.get_count()}")

        # Start clipboard listener
        self.listener.start()

        # Capture initial clipboard state immediately on startup
        threading.Thread(target=self.listener._on_clipboard_change, daemon=True).start()

        # Create tray icon
        icon_image = create_tray_icon_image()
        self.tray_icon = pystray.Icon(
            name="ClipboardManager",
            icon=icon_image,
            title="Clipboard Manager",
            menu=pystray.Menu(
                pystray.MenuItem("Open Manager", self._on_open, default=True),
                pystray.MenuItem("Settings", self._on_settings),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Clear History", self._on_clear),
                pystray.MenuItem("Export to Markdown", self._on_export),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )

        # Run tray in a separate thread
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

        # Run tkinter main loop
        self.gui._tk_root = True
        root = tk.Tk()
        root.withdraw()  # Hidden root window

        # Create the manager window but hidden initially
        self.gui.root = root

        def periodic_check():
            if self._running:
                root.after(500, periodic_check)

        periodic_check()
        root.mainloop()


if __name__ == "__main__":
    app = ClipboardManagerApp()
    app.run()
