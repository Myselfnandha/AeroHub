# ruff: noqa: E402

import tkinter as tk
import threading

# Categorized emojis for the picker
EMOJI_CATEGORIES = {
    "Smileys": [
        "😀",
        "😃",
        "😄",
        "😁",
        "😆",
        "😅",
        "😂",
        "🤣",
        "😊",
        "😇",
        "🙂",
        "🙃",
        "😉",
        "😌",
        "😍",
        "🥰",
        "😘",
        "😗",
        "😙",
        "😚",
        "😋",
        "😛",
        "😝",
        "😜",
        "🤪",
        "🤨",
        "🧐",
        "🤓",
        "😎",
        "🤩",
        "🥳",
        "😏",
        "😒",
        "😞",
        "😔",
        "😟",
        "😕",
        "🙁",
        "☹️",
        "😣",
        "😖",
        "😫",
        "😩",
        "🥺",
        "😢",
        "😭",
        "😤",
        "😠",
        "😡",
        "🤬",
        "🤯",
        "😳",
        "🥵",
        "🥶",
        "😱",
        "😨",
        "😰",
        "😥",
        "😓",
        "🤗",
        "🤔",
        "🤭",
        "🤫",
        "🤥",
        "😶",
        "😐",
        "😑",
        "😬",
        "🙄",
        "😯",
        "😦",
        "😧",
        "😮",
        "😲",
        "🥱",
        "😴",
        "🤤",
        "😪",
        "😵",
        "🤐",
        "🥴",
        "🤢",
        "🤮",
        "🤧",
        "😷",
        "🤒",
        "🤕",
        "🤑",
        "🤠",
        "😈",
        "👿",
        "👹",
        "👺",
        "🤡",
        "💩",
        "👻",
        "💀",
        "☠️",
        "👽",
        "👾",
        "🤖",
        "🎃",
        "😺",
        "😸",
        "😹",
        "😻",
        "😼",
        "😽",
        "🙀",
        "😿",
        "😾",
    ],
    "Gestures": [
        "👋",
        "🤚",
        "🖐️",
        "✋",
        "🖖",
        "👌",
        "🤏",
        "✌️",
        "🤞",
        "🤟",
        "🤘",
        "🤙",
        "👈",
        "👉",
        "👆",
        "🖕",
        "👇",
        "☝️",
        "👍",
        "👎",
        "✊",
        "👊",
        "🤛",
        "🤜",
        "👏",
        "🙌",
        "👐",
        "🤲",
        "🤝",
        "🙏",
        "✍️",
        "💅",
        "🤳",
        "💪",
        "🦾",
        "🦵",
        "🦿",
        "🦶",
        "👂",
        "🦻",
        "👃",
        "🧠",
        "🦷",
        "🦴",
        "👀",
        "👁️",
        "👅",
        "👄",
        "💋",
        "🩸",
    ],
    "Objects & Tech": [
        "💻",
        "🖥️",
        "🖨️",
        "⌨️",
        "🖱️",
        "🖲️",
        "💽",
        "💾",
        "💿",
        "📀",
        "🧮",
        "🎥",
        "🎞️",
        "📽️",
        "🎬",
        "📺",
        "📷",
        "📸",
        "📹",
        "📼",
        "🔍",
        "🔎",
        "🕯️",
        "💡",
        "🔦",
        "🏮",
        "📔",
        "📕",
        "📖",
        "📗",
        "📘",
        "📙",
        "📚",
        "📓",
        "📒",
        "📃",
        "📜",
        "📄",
        "📰",
        "🗞️",
        "📑",
        "🔖",
        "🏷️",
        "💰",
        "🪙",
        "💴",
        "💵",
        "💶",
        "💷",
        "💸",
        "💳",
        "🧾",
        "✉️",
        "📧",
        "📨",
        "📩",
        "📤",
        "📥",
        "📦",
        "📫",
        "📪",
        "📬",
        "📭",
        "📮",
        "🗳️",
        "✏️",
        "✒️",
        "🖋️",
        "🖊️",
        "🖌️",
        "🖍️",
        "📝",
        "💼",
        "📁",
        "📂",
        "🗂️",
        "📅",
        "📆",
        "🗒️",
        "🗓️",
        "📇",
        "📈",
        "📉",
        "📊",
        "📋",
        "📌",
        "📍",
        "📎",
        "🖇️",
        "📏",
        "📐",
        "✂️",
        "🗃️",
        "🗄️",
        "🗑️",
        "🔒",
        "🔓",
        "🔏",
        "🔐",
        "🔑",
        "🗝️",
        "🔨",
        "🪓",
        "⛏️",
        "⚒️",
        "🛠️",
        "🗡️",
        "⚔️",
        "🔫",
        "🏹",
        "🛡️",
        "🔧",
        "🔩",
        "⚙️",
        "🗜️",
        "⚖️",
        "🦯",
        "🔗",
        "⛓️",
        "🧰",
        "🧲",
        "⚗️",
        "🧪",
        "🧫",
        "🧬",
        "🔬",
        "🔭",
        "📡",
        "💉",
        "🩸",
        "💊",
        "🩹",
        "🩺",
        "🚪",
        "🛏️",
        "🛋️",
        "🪑",
        "🚽",
        "🚿",
        "🛁",
        "🪒",
        "🧴",
        "🧷",
        "🧹",
        "🧺",
        "🧻",
        "🧼",
        "🧽",
        "🧯",
        "🛒",
        "🚬",
        "⚰️",
        "⚱️",
        "🗿",
    ],
    "Symbols": [
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "🤍",
        "🤎",
        "💔",
        "❣️",
        "💕",
        "💞",
        "💓",
        "💗",
        "💖",
        "💘",
        "💝",
        "💟",
        "☮️",
        "✝️",
        "☪️",
        "🕉️",
        "☸️",
        "✡️",
        "🔯",
        "🕎",
        "☯️",
        "☦️",
        "🛐",
        "⛎",
        "♈",
        "♉",
        "♊",
        "♋",
        "♌",
        "♍",
        "♎",
        "♏",
        "♐",
        "♑",
        "♒",
        "♓",
        "🆔",
        "⚛️",
        "⚕️",
        "☢️",
        "☣️",
        "📴",
        "📳",
        "🈶",
        "🈚",
        "🈸",
        "🈺",
        "🈷️",
        "✴️",
        "🆚",
        "🉑",
        "💮",
        "🉐",
        "㊙️",
        "㊗️",
        "🈴",
        "🈵",
        "🈹",
        "🈲",
        "🅰️",
        "🅱️",
        "🆎",
        "🆑",
        "🅾️",
        "🆘",
        "❌",
        "⭕",
        "🛑",
        "⛔",
        "📛",
        "🚫",
        "💯",
        "💢",
        "♨️",
        "🚷",
        "🚯",
        "🚳",
        "🚱",
        "🔞",
        "📵",
        "🚭",
        "❗",
        "❕",
        "❓",
        "❔",
        "‼️",
        "⁉️",
        "🔅",
        "🔆",
        "〽️",
        "⚠️",
        "🚸",
        "🔱",
        "⚜️",
        "🔰",
        "♻️",
        "✅",
        "🈯",
        "💹",
        "❇️",
        "✳️",
        "❎",
        "🌐",
        "💠",
        "Ⓜ️",
        "🌀",
        "💤",
        "🏧",
        "🚾",
        "♿",
        "🅿️",
        "🈳",
        "🈂️",
        "🛂",
        "🛃",
        "🛄",
        "🛅",
        "🚹",
        "🚺",
        "🚼",
        "🚻",
        "🚮",
        "🎦",
        "📶",
        "🈁",
        "🔣",
        "ℹ️",
        "🔤",
        "🔡",
        "🔠",
        "🆖",
        "🆗",
        "🆙",
        "🆒",
        "🆕",
        "🆓",
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟",
        "🔢",
        "#️⃣",
        "*️⃣",
        "⏏️",
        "▶️",
        "⏸️",
        "⏯️",
        "⏹️",
        "⏺️",
        "⏭️",
        "⏮️",
        "⏩",
        "⏪",
        "⏫",
        "⏬",
        "◀️",
        "🔼",
        "🔽",
        "➡️",
        "⬅️",
        "⬆️",
        "⬇️",
        "↗️",
        "↘️",
        "↙️",
        "↖️",
        "↕️",
        "↔️",
        "↪️",
        "↩️",
        "⤴️",
        "⤵️",
        "🔀",
        "🔁",
        "🔂",
        "🔄",
        "🔃",
        "🎵",
        "🎶",
        "➕",
        "➖",
        "➗",
        "✖️",
        "♾️",
        "💲",
        "💱",
        "™️",
        "©️",
        "®️",
        "〰️",
        "➰",
        "➿",
        "🔚",
        "🔙",
        "🔛",
        "🔝",
        "🔜",
        "✔️",
        "☑️",
        "🔘",
        "🔴",
        "🟠",
        "🟡",
        "🟢",
        "🔵",
        "🟣",
        "⚫",
        "⚪",
        "🟤",
        "🔺",
        "🔻",
        "🔸",
        "🔹",
        "🔶",
        "🔷",
        "🔳",
        "🔲",
        "▪️",
        "▫️",
        "◾",
        "◽",
        "◼️",
        "◻️",
        "🟥",
        "🟧",
        "🟨",
        "🟩",
        "🟦",
        "🟪",
        "⬛",
        "⬜",
        "🟫",
        "🔈",
        "🔇",
        "🔉",
        "🔊",
        "🔔",
        "🔕",
        "📣",
        "📢",
        "💬",
        "💭",
        "🗯️",
        "♠️",
        "♣️",
        "♥️",
        "♦️",
        "🃏",
        "🎴",
        "🀄",
        "🕐",
        "🕑",
        "🕒",
        "🕓",
        "🕔",
        "🕕",
        "🕖",
        "🕗",
        "🕘",
        "🕙",
        "🕚",
        "🕛",
        "🕜",
        "🕝",
        "🕞",
        "🕟",
        "🕠",
        "🕡",
        "🕢",
        "🕣",
        "🕤",
        "🕥",
        "🕦",
        "🕧",
    ],
}


class EmojiPickerPanel(tk.Toplevel):
    """A popup window to pick an emoji."""

    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        self.on_select_callback = on_select_callback

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(
            bg="#1e1e1e",
            padx=2,
            pady=2,
            highlightthickness=1,
            highlightbackground="#3e3e3e",
        )

        # Determine position near cursor
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        self.geometry(f"340x260+{x}+{y}")

        # Title bar
        title_frame = tk.Frame(self, bg="#2d2d2d", height=24)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Select Emoji",
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT, padx=8)
        close_btn = tk.Button(
            title_frame,
            text="✕",
            bg="#2d2d2d",
            fg="#ffffff",
            relief=tk.FLAT,
            bd=0,
            command=self.destroy,
            font=("Segoe UI", 9),
        )
        close_btn.pack(side=tk.RIGHT, padx=4)

        # Tabs
        self.tab_frame = tk.Frame(self, bg="#1e1e1e")
        self.tab_frame.pack(fill=tk.X, pady=2)

        # Content frame
        self.content_frame = tk.Frame(self, bg="#1e1e1e")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.canvases = {}
        self.current_tab = None
        self.tab_buttons = {}

        for cat in EMOJI_CATEGORIES.keys():
            btn = tk.Button(
                self.tab_frame,
                text=cat,
                bg="#1e1e1e",
                fg="#a0a0a0",
                relief=tk.FLAT,
                bd=0,
                font=("Segoe UI", 8),
                command=lambda c=cat: self.show_category(c),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tab_buttons[cat] = btn

            # Create a canvas with scrollbar for each category
            f = tk.Frame(self.content_frame, bg="#1e1e1e")
            canvas = tk.Canvas(f, bg="#1e1e1e", highlightthickness=0)
            scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                ),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Grid of emojis
            col = 0
            row = 0
            for emoji in EMOJI_CATEGORIES[cat]:
                ebtn = tk.Button(
                    scrollable_frame,
                    text=emoji,
                    font=("Segoe UI Emoji", 14),
                    bg="#1e1e1e",
                    fg="#ffffff",
                    relief=tk.FLAT,
                    bd=0,
                    activebackground="#3e3e3e",
                    cursor="hand2",
                    command=lambda e=emoji: self.select_emoji(e),
                )
                ebtn.grid(row=row, column=col, padx=2, pady=2)
                col += 1
                if col > 8:
                    col = 0
                    row += 1

            # Enable mouse wheel scrolling
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

            self.bind_all("<MouseWheel>", _on_mousewheel)

            canvas.pack(side="left", fill="both", expand=True)

            self.canvases[cat] = f

        # Show first category
        self.show_category(list(EMOJI_CATEGORIES.keys())[0])

    def show_category(self, cat):
        if self.current_tab:
            self.canvases[self.current_tab].pack_forget()
            self.tab_buttons[self.current_tab].config(fg="#a0a0a0", bg="#1e1e1e")

        self.canvases[cat].pack(fill=tk.BOTH, expand=True)
        self.tab_buttons[cat].config(fg="#ffffff", bg="#3e3e3e")
        self.current_tab = cat

    def select_emoji(self, emoji):
        self.on_select_callback(emoji)
        self.destroy()

    def destroy(self):
        try:
            self.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()


import os
import json
import time
import psutil

# Path to cross-process toast status file in the UTILITIES directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(SCRIPT_DIR, "toast_status.json")

def read_shared_status() -> dict:
    if not os.path.exists(STATUS_FILE):
        return {}
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def write_shared_status(status: dict):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)
    except Exception:
        pass

def is_process_running(pid: int) -> bool:
    if not pid:
        return False
    try:
        return psutil.pid_exists(pid)
    except Exception:
        return False

def is_any_toast_active() -> bool:
    status = read_shared_status()
    pid = status.get("active_toast_pid")
    end_time = status.get("active_toast_end_time", 0.0)
    
    # If break overlay is active, block toasts
    if status.get("break_active") and is_process_running(status.get("break_pid")):
        return True
        
    # If another process's toast is active, block toasts
    if pid and pid != os.getpid() and is_process_running(pid) and time.time() < end_time:
        return True
        
    return False

def is_in_break_period_shared() -> bool:
    status = read_shared_status()
    now = time.time()
    
    # 1. Break warning active
    if status.get("break_warning_active") and is_process_running(status.get("break_warning_pid")):
        if now < status.get("break_warning_end_time", 0.0):
            return True
            
    # 2. Break active
    if status.get("break_active") and is_process_running(status.get("break_pid")):
        return True
        
    # 3. Within 10 seconds after a break ended
    last_end = status.get("last_break_end_time", 0.0)
    if now - last_end < 10.0:
        return True
        
    return False


class ToastQueue:
    _lock = threading.RLock()
    _queue = []
    _active = None
    _delay_active = False

    @classmethod
    def add(cls, toast):
        with cls._lock:
            cls._queue.append(toast)
            
        # Signal any active toasts in other processes to close
        try:
            status = read_shared_status()
            status["request_dismiss_at"] = time.time()
            status["dismiss_sender_id"] = toast.toast_id
            write_shared_status(status)
        except Exception:
            pass

        # Signal active toasts in this process to close immediately
        with BaseToast._lock:
            for active_toast in list(BaseToast._active_toasts):
                if hasattr(active_toast, "cleanup"):
                    try:
                        active_toast.cleanup()
                    except Exception:
                        pass

        cls.process_queue()

    @classmethod
    def process_queue(cls):
        with cls._lock:
            if cls._active or cls._delay_active:
                return
            if not cls._queue:
                return
            
            # Check if another process has an active toast or break
            if is_any_toast_active():
                next_toast = cls._queue[0]
                if next_toast.parent:
                    try:
                        next_toast.parent.after(500, cls.process_queue)
                        return
                    except Exception:
                        pass
                import threading
                timer = threading.Timer(0.5, cls.process_queue)
                timer.daemon = True
                timer.start()
                return

            cls._active = cls._queue.pop(0)

        try:
            cls._active._create_toast()
        except Exception as e:
            print(f"Error creating queued toast: {e}")
            cls.on_toast_closed(None)

    @classmethod
    def on_toast_closed(cls, parent):
        with cls._lock:
            cls._active = None
            cls._delay_active = True

        # Check if we have more toasts queued
        has_waiting = False
        with cls._lock:
            if cls._queue:
                has_waiting = True

        # Fast transition (100ms) if another toast is queued, otherwise normal spacing (1.5s)
        delay_ms = 100 if has_waiting else 1500

        def reset_delay():
            with cls._lock:
                cls._delay_active = False
            cls.process_queue()

        if parent:
            try:
                parent.after(delay_ms, reset_delay)
                return
            except Exception:
                pass

        try:
            if BaseToast._root:
                BaseToast._root.after(delay_ms, reset_delay)
                return
        except Exception:
            pass

        timer = threading.Timer(delay_ms / 1000.0, reset_delay)
        timer.daemon = True
        timer.start()


class BaseToast:
    """
    A highly customizable unified toast notification class.
    Supports 9 positions, 7 animations, shadows, gradients, and behavioral settings.
    """

    _active_toasts = []
    _lock = threading.RLock()
    _root = None

    def __init__(
        self,
        parent,
        title: str,
        message: str,
        settings: dict,
        is_health_tip: bool = False,
        on_click=None,
    ):
        self.parent = parent
        self.title = title
        self.message = message
        self.settings = settings
        self.is_health_tip = is_health_tip
        self.on_click = on_click
        self.closing = False
        self.toast_window = None
        self.hold_time = 0
        self.slot_index = 0
        self.pos = "center"
        import uuid
        self.toast_id = str(uuid.uuid4())
        self.created_at = time.time()

    def show(self):
        try:
            # Skip if we are in the break period, unless this is a break warning itself
            is_break_warning = "break in" in self.title.lower() or "break in" in self.message.lower() or "eye break" in self.title.lower()
            if not is_break_warning and is_in_break_period_shared():
                print(f"Discarding toast '{self.title}' because we are in a break period.")
                return
            if self.settings.get("is_preview", False):
                self._create_toast()
                return
            ToastQueue.add(self)
        except Exception as e:
            print(f"Error queuing toast: {e}")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (0, 0, 0)

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def interpolate_color(self, c1, c2, factor):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3))

    def _create_toast(self):
        # Signal any other active toasts to dismiss cross-process
        try:
            status = read_shared_status()
            status["request_dismiss_at"] = time.time()
            status["dismiss_sender_id"] = self.toast_id
            write_shared_status(status)
        except Exception:
            pass

        root = self.parent
        if not root:
            root = tk.Tk()
            root.withdraw()
        BaseToast._root = root

        toast = tk.Toplevel(root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        trans_color = "#010203"
        toast.configure(bg=trans_color)
        toast.attributes("-transparentcolor", trans_color)
        toast.attributes("-alpha", 0.0)

        # Retrieve visual settings
        prefix = "ht_toast_" if self.is_health_tip else "toast_"
        tw = int(self.settings.get(f"{prefix}width", 260))
        th = int(self.settings.get(f"{prefix}height", 60))
        pos = self.settings.get(f"{prefix}pos", "Center").lower()
        if pos == "random":
            import random

            pos = random.choice(
                [
                    "top-left",
                    "top-center",
                    "top-right",
                    "bottom-left",
                    "bottom-center",
                    "bottom-right",
                    "middle-left",
                    "middle-right",
                ]
            )
        bg_col = self.settings.get(f"{prefix}bg_color", "#252525")
        fg_col = self.settings.get(f"{prefix}fg_color", "#ffffff")
        accent_default = "#00f0ff" if prefix in ("toast_", "ht_toast_") else "#7c3aed"
        accent_col = self.settings.get(f"{prefix}accent_color", accent_default)
        font_size = int(self.settings.get(f"{prefix}font_size", 11))
        font_weight = self.settings.get(f"{prefix}font_weight", "bold")
        font_family = self.settings.get(f"{prefix}font_family", "Segoe UI")
        emoji = self.settings.get(f"{prefix}emoji", "👁️")
        radius = int(self.settings.get(f"{prefix}radius", 16))
        padx = int(self.settings.get(f"{prefix}padding_x", 12))
        pady = int(self.settings.get(f"{prefix}padding_y", 10))
        anim_style = self.settings.get(f"{prefix}anim_style", "Slide").lower()
        target_opacity = float(self.settings.get(f"{prefix}opacity", 0.92))
        border_width = int(self.settings.get(f"{prefix}border_width", 0))
        border_color = self.settings.get(f"{prefix}border_color", accent_default)

        # ── Sanitize settings ──
        # Clamp opacity to valid range
        target_opacity = max(0.0, min(1.0, target_opacity))

        # Fallback empty color strings to defaults
        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = accent_default
        if not border_color or not border_color.startswith("#"):
            border_color = accent_default
        if not emoji:
            emoji = "👁️" if not self.is_health_tip else "💡"

        # Prevent any color from matching the transparent key color
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if accent_col == trans_color:
            accent_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"

        # Clamp padding so text doesn't render off-canvas
        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        # New visual features
        _enable_gradient = self.settings.get(f"{prefix}gradient", False)
        enable_shadow = self.settings.get(f"{prefix}shadow", True)
        accent_stripe = self.settings.get(f"{prefix}accent_stripe", False)
        text_align = self.settings.get(f"{prefix}text_align", "left")

        # Behavioral settings
        transition_ms = int(self.settings.get(f"{prefix}transition_time_ms", 320))
        transition_sec = max(0.01, transition_ms / 1000.0)

        if self.is_health_tip:
            duration_sec = float(self.settings.get(f"{prefix}duration_sec", self.settings.get("ht_duration_sec", 5)))
        else:
            duration_sec = float(self.settings.get(
                f"{prefix}duration_sec", self.settings.get(f"{prefix}duration", self.settings.get("pre_warning_sec", 5))
            ))
        auto_dismiss = self.settings.get(f"{prefix}auto_dismiss", True)
        click_action = self.settings.get(f"{prefix}click_action", "dismiss")

        # Register this toast in cross-process shared status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        status["active_toast_end_time"] = time.time() + (duration_sec if auto_dismiss else 999999) + 2
        write_shared_status(status)

        shadow_offset = 6 if enable_shadow else 0
        canvas_w = tw + shadow_offset * 2
        canvas_h = th + shadow_offset * 2

        # Screen positions (9 points)
        sw = toast.winfo_screenwidth()
        sh = toast.winfo_screenheight()
        padding_edge = 20

        fx, fy = 0, 0
        if "top" in pos or pos in ("left", "center", "right"):
            fy = padding_edge
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "bottom" in pos:
            fy = sh - th - 50  # account for taskbar
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "middle" in pos:
            fy = (sh - th) // 2
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        else:
            # custom offset
            fx = int(self.settings.get(f"{prefix}custom_x", (sw - tw) // 2))
            fy = int(self.settings.get(f"{prefix}custom_y", padding_edge))

        self.pos = pos
        # Adjust for multiple toasts stacking
        with BaseToast._lock:
            # Find the first available slot index for this position to prevent overlap
            occupied_slots = {
                t.slot_index
                for t in BaseToast._active_toasts
                if getattr(t, "pos", None) == self.pos
            }
            self.slot_index = 0
            while self.slot_index in occupied_slots:
                self.slot_index += 1

            y_offset = self.slot_index * (th + 10)
            if "bottom" in self.pos:
                fy -= y_offset
            else:
                fy += y_offset
            BaseToast._active_toasts.append(self)
            self.toast_window = toast

        # Animation start points
        sx, sy = fx, fy
        if anim_style == "slide":
            if "left" in pos:
                sx = -tw - shadow_offset
            elif "right" in pos:
                sx = sw + shadow_offset
            elif "top" in pos or pos == "center":
                sy = -th - shadow_offset
            elif "bottom" in pos:
                sy = sh + shadow_offset
        elif anim_style == "drop":
            sy = -th - 100
        elif anim_style == "bounce":
            if "left" in pos:
                sx = -tw - 50
            elif "right" in pos:
                sx = sw + 50
            else:
                sy = -th - 50

        toast.geometry(f"{canvas_w}x{canvas_h}+{sx}+{sy}")

        canvas = tk.Canvas(
            toast, width=canvas_w, height=canvas_h, bg=trans_color, highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas = canvas

        def create_round_poly(x, y, w, h, r):
            return [
                x + r,
                y,
                w - r,
                y,
                w,
                y,
                w,
                y + r,
                w,
                h - r,
                w,
                h,
                w - r,
                h,
                x + r,
                h,
                x,
                h,
                x,
                h - r,
                x,
                y + r,
                x,
                y,
            ]

        # Shadow
        shadow_id = None
        if enable_shadow:
            shadow_poly = create_round_poly(
                shadow_offset,
                shadow_offset,
                tw + shadow_offset,
                th + shadow_offset,
                radius,
            )
            shadow_id = canvas.create_polygon(shadow_poly, smooth=True, fill="#080808")

        bg_poly = create_round_poly(
            shadow_offset // 2,
            shadow_offset // 2,
            tw + shadow_offset // 2,
            th + shadow_offset // 2,
            radius,
        )

        border_style = self.settings.get(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)

        bg_id = canvas.create_polygon(
            bg_poly,
            smooth=True,
            fill=bg_col,
            outline=border_color,
            width=border_width,
            dash=dash_val,
        )

        # Accent Stripe
        stripe_id = None
        if accent_stripe:
            stripe_pos = self.settings.get(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    tw + shadow_offset // 2 - radius - 4, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + radius,
                    tw + shadow_offset // 2, th + shadow_offset // 2 - radius,
                    tw + shadow_offset // 2 - radius - 4, th + shadow_offset // 2,
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    tw + shadow_offset // 2 - radius, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + 4,
                    shadow_offset // 2, shadow_offset // 2 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    shadow_offset // 2 + radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2 - radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2
                ]
            else: # Left
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, th + shadow_offset // 2,
                    shadow_offset // 2 + radius, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2 - radius,
                    shadow_offset // 2, shadow_offset // 2 + radius
                ]
            stripe_id = canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        # Content
        msg_font = (font_family, font_size, font_weight)
        sub_font = (font_family, max(8, font_size - 2))

        # Fallback font for emojis (moved to execute before rendering text)
        if msg_font[0] == "Segoe UI" or msg_font[0] == "Segoe UI Emoji":
            msg_font = (
                "Segoe UI Emoji",
                msg_font[1],
                msg_font[2] if len(msg_font) > 2 else "normal",
            )

        anchor = tk.W
        tx = shadow_offset // 2 + padx + 10
        if text_align == "center":
            anchor = tk.CENTER
            tx = shadow_offset // 2 + tw // 2
        elif text_align == "right":
            anchor = tk.E
            tx = shadow_offset // 2 + tw - padx - 10

        desc_text_id = None
        
        # Add clock time if enabled
        show_clock = self.settings.get(f"{prefix}show_clock", False)
        clock_str = f" - {time.strftime('%I:%M %p')}" if show_clock else ""
        
        if self.is_health_tip:
            text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + th // 2,
                anchor=anchor,
                text=f"{emoji}  {self.message}{clock_str}",
                font=msg_font,
                fill=fg_col,
                width=tw - (padx + 10) * 2,
            )
        else:
            text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + pady,
                anchor=anchor,
                text=f"{emoji}  {self.title}{clock_str}",
                font=msg_font,
                fill=fg_col,
            )
            desc_text_id = canvas.create_text(
                tx,
                shadow_offset // 2 + pady + font_size + 8,
                anchor=anchor,
                text=self.message,
                font=sub_font,
                fill="#8892b0",
                width=tw - (padx + 10) * 2,
            )

        # Progress bar
        show_progress = self.settings.get(f"{prefix}progress_bar", False)
        progress_bar = None
        if show_progress and auto_dismiss and duration_sec > 0:
            bar_y = shadow_offset // 2 + th - 4
            progress_bar = canvas.create_rectangle(
                shadow_offset // 2 + radius,
                bar_y,
                shadow_offset // 2 + tw - radius,
                bar_y + 2,
                fill=accent_col,
                outline="",
            )

        # Interaction
        self._drag_data = {"x": 0, "y": 0, "dragged": False}

        def on_press(event):
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
            self._drag_data["dragged"] = False

        def on_drag(event):
            dx = event.x_root - self._drag_data["x"]
            dy = event.y_root - self._drag_data["y"]
            if abs(dx) > 3 or abs(dy) > 3:
                self._drag_data["dragged"] = True
            x = toast.winfo_x() + dx
            y = toast.winfo_y() + dy
            toast.geometry(f"+{x}+{y}")
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root

        def on_click_event(event):
            if self._drag_data.get("dragged"):
                return
            self.force_close()  # Always dismiss immediately on click
            if click_action == "snooze":
                if self.on_click:
                    self.on_click("snooze")
            elif click_action == "settings":
                if self.on_click:
                    self.on_click("settings")
            elif click_action != "dismiss":
                if self.on_click:
                    self.on_click("custom")

        toast.bind("<ButtonPress-1>", on_press)
        toast.bind("<B1-Motion>", on_drag)
        toast.bind("<ButtonRelease-1>", on_click_event)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_click_event)

        self.is_hovered = False

        def on_enter(e):
            self.is_hovered = True

        def on_leave(e):
            self.is_hovered = False

        toast.bind("<Enter>", on_enter)
        toast.bind("<Leave>", on_leave)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

        # Emoji fallback check moved above

        # Adjust height if text is too tall
        original_th = th
        if self.is_health_tip:
            bbox = canvas.bbox(text_id)
            if bbox and (bbox[3] - bbox[1] > th - 20):
                th = bbox[3] - bbox[1] + 20
                canvas_h = th + shadow_offset
                toast.geometry(f"{canvas_w}x{canvas_h}")
                canvas.configure(height=canvas_h)
                canvas.coords(text_id, tx, shadow_offset // 2 + th // 2)
        else:
            bbox_title = canvas.bbox(text_id)
            bbox_desc = canvas.bbox(desc_text_id)
            if bbox_title and bbox_desc:
                title_h = bbox_title[3] - bbox_title[1]
                desc_h = bbox_desc[3] - bbox_desc[1]
                total_needed = pady + title_h + 8 + desc_h + pady
                if total_needed > th:
                    th = total_needed
                    canvas_h = th + shadow_offset
                    toast.geometry(f"{canvas_w}x{canvas_h}")
                    canvas.configure(height=canvas_h)
                    desc_y = bbox_title[3] + 8 + desc_h // 2
                    canvas.coords(desc_text_id, tx, desc_y)

        # Update background and shadow polygons if height adjusted
        if th > original_th:
            new_bg_poly = create_round_poly(
                shadow_offset // 2,
                shadow_offset // 2,
                tw + shadow_offset // 2,
                th + shadow_offset // 2,
                radius,
            )
            canvas.coords(bg_id, *new_bg_poly)
            if shadow_id:
                new_shadow_poly = create_round_poly(
                    shadow_offset,
                    shadow_offset,
                    tw + shadow_offset,
                    th + shadow_offset,
                    radius,
                )
                canvas.coords(shadow_id, *new_shadow_poly)
            if stripe_id:
                new_stripe_poly = [
                    shadow_offset // 2 + radius,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius + 4,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius + 4,
                    th + shadow_offset // 2,
                    shadow_offset // 2 + radius,
                    th + shadow_offset // 2,
                    shadow_offset // 2,
                    th + shadow_offset // 2 - radius,
                    shadow_offset // 2,
                    shadow_offset // 2 + radius,
                ]
                canvas.coords(stripe_id, *new_stripe_poly)
            if progress_bar:
                bar_y = shadow_offset // 2 + th - 4
                canvas.coords(
                    progress_bar,
                    shadow_offset // 2 + radius,
                    bar_y,
                    shadow_offset // 2 + tw - radius,
                    bar_y + 2,
                )

        # Typewriter effect helper
        if anim_style == "typewriter":
            if self.is_health_tip:
                full_text = f"{emoji}  {self.message}"
                canvas.itemconfig(text_id, text="")

                def type_char(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_text):
                        canvas.itemconfig(text_id, text=full_text[:idx])
                        toast.after(30, lambda: type_char(idx + 1))

                toast.after(200, type_char)
            else:
                full_title = f"{emoji}  {self.title}"
                canvas.itemconfig(text_id, text="")
                full_desc = self.message
                canvas.itemconfig(desc_text_id, text="")

                def type_desc(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_desc):
                        canvas.itemconfig(desc_text_id, text=full_desc[:idx])
                        toast.after(20, lambda: type_desc(idx + 1))

                def type_title(idx=0):
                    if self.closing:
                        return
                    if idx <= len(full_title):
                        canvas.itemconfig(text_id, text=full_title[:idx])
                        toast.after(30, lambda: type_title(idx + 1))
                    else:
                        toast.after(100, lambda: type_desc(0))

                toast.after(200, type_title)

        # Animations
        self.start_time = time.perf_counter()

        def animate_in():
            if self.closing:
                return
            try:
                elapsed = time.perf_counter() - self.start_time
                p = min(1.0, elapsed / transition_sec)

                if anim_style == "fade" or anim_style == "typewriter":
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    toast.attributes("-alpha", p * target_opacity)
                elif anim_style == "slide":
                    ease = 1 - (1 - p) ** 3
                    cx = int(sx + (fx - sx) * ease)
                    cy = int(sy + (fy - sy) * ease)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{cx}+{cy}")
                    toast.attributes("-alpha", target_opacity)
                elif anim_style == "bounce":
                    ease = 1 - (1 - p) ** 3
                    # Add elastic overshoot
                    if p < 0.8:
                        overshoot = 1.1 * (p / 0.8)
                    else:
                        overshoot = 1.1 - 0.1 * ((p - 0.8) / 0.2)
                    cx = int(sx + (fx - sx) * overshoot)
                    cy = int(sy + (fy - sy) * overshoot)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{cx}+{cy}")
                    toast.attributes("-alpha", target_opacity)
                elif anim_style == "scale":
                    ease = p
                    cy = int(fy + 10 * (1 - ease))
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{cy}")
                    toast.attributes("-alpha", p * target_opacity)
                elif anim_style == "glow":
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    glow_a = (
                        target_opacity
                        if int(elapsed * 10) % 2 == 0
                        else target_opacity * 0.5
                    )
                    toast.attributes("-alpha", glow_a)
                elif anim_style == "drop":
                    ease = p * p  # accelerate
                    cy = int(sy + (fy - sy) * ease)
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{cy}")
                    toast.attributes("-alpha", p * target_opacity)
                else:
                    # Default fallback
                    toast.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
                    toast.attributes("-alpha", target_opacity)

                if p < 1.0:
                    toast.after(16, animate_in)
                else:
                    if anim_style == "glow":
                        toast.attributes("-alpha", target_opacity)  # settle
                    update_progress()
            except Exception:
                self.cleanup()

        self.hover_time = 0

        def update_progress():
            if self.closing:
                return
            try:
                # Check cross-process / new toast dismissal signal
                status = read_shared_status()
                req_dismiss_at = status.get("request_dismiss_at", 0.0)
                dismiss_sender_id = status.get("dismiss_sender_id", "")
                if req_dismiss_at > self.created_at and dismiss_sender_id != self.toast_id:
                    self.out_start_time = time.perf_counter()
                    animate_out()
                    return

                if auto_dismiss and duration_sec > 0:
                    if not self.is_hovered or self.hover_time > 15000:
                        self.hold_time += 50
                        if show_progress and progress_bar:
                            p = self.hold_time / (duration_sec * 1000)
                            cur_w = (tw - radius * 2) * (1 - p)
                            if cur_w > 0:
                                canvas.coords(
                                    progress_bar,
                                    shadow_offset // 2 + radius,
                                    bar_y,
                                    shadow_offset // 2 + radius + cur_w,
                                    bar_y + 2,
                                )

                        if self.hold_time >= duration_sec * 1000:
                            self.out_start_time = time.perf_counter()
                            animate_out()
                            return
                    else:
                        self.hover_time += 50
                toast.after(50, update_progress)
            except Exception:
                self.cleanup()

        def animate_out():
            self.closing = True
            try:
                if not hasattr(self, 'out_start_time'):
                    self.out_start_time = time.perf_counter()
                
                elapsed = time.perf_counter() - self.out_start_time
                p = max(0.0, 1.0 - (elapsed / transition_sec))
                
                toast.attributes("-alpha", p * target_opacity)
                if p > 0:
                    toast.after(16, animate_out)
                else:
                    self.cleanup()
            except Exception:
                self.cleanup()

        self.force_close = animate_out

        toast.deiconify()
        animate_in()

        # Play sound if applicable
        play_sound = self.settings.get(f"{prefix}enable_sound", False)
        if play_sound:
            self._play_sound()

    def _play_sound(self):
        try:
            import os
            prefix = "ht_toast_" if self.is_health_tip else "toast_"
            default_snd = "mac_disconnect" if self.is_health_tip else "mac_connect"
            snd_choice = self.settings.get(f"{prefix}sound_effect", default_snd)
            volume = float(self.settings.get(f"{prefix}volume", 80))

            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]

            is_alias = snd_choice in system_aliases
            if not is_alias:
                if not snd_choice.endswith(".wav"):
                    snd_choice += ".wav"
                script_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(os.path.dirname(script_dir), "health_app", "resources", "sounds", snd_choice)
                if not os.path.exists(path):
                    path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "toggles", "battery_monitor", "sounds", snd_choice)
                if not os.path.exists(path):
                    path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "toggles", "temp_monitor", "sounds", snd_choice)
            else:
                path = None

            # Try playing using Pygame Sound if pygame is active/initialized
            try:
                import pygame
                if pygame.mixer.get_init() and path and os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(volume / 100.0)
                    sound.play()
                    return
            except Exception:
                pass

            # Fallback to winsound
            import winsound
            if is_alias:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
            elif path and os.path.exists(path):
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def update_settings(self, settings):
        self.settings = settings
        if not self.toast_window or not self.toast_window.winfo_exists():
            return
            
        prefix = "ht_toast_" if self.is_health_tip else "toast_"
        tw = int(self.settings.get(f"{prefix}width", 260))
        th = int(self.settings.get(f"{prefix}height", 60))
        pos = self.settings.get(f"{prefix}pos", "Center").lower()
        if pos == "random":
            pos = "center"
        bg_col = self.settings.get(f"{prefix}bg_color", "#252525")
        fg_col = self.settings.get(f"{prefix}fg_color", "#ffffff")
        accent_default = "#00f0ff" if prefix in ("toast_", "ht_toast_") else "#7c3aed"
        accent_col = self.settings.get(f"{prefix}accent_color", accent_default)
        font_size = int(self.settings.get(f"{prefix}font_size", 11))
        font_weight = self.settings.get(f"{prefix}font_weight", "bold")
        font_family = self.settings.get(f"{prefix}font_family", "Segoe UI")
        emoji = self.settings.get(f"{prefix}emoji", "👁️")
        radius = int(self.settings.get(f"{prefix}radius", 16))
        padx = int(self.settings.get(f"{prefix}padding_x", 12))
        pady = int(self.settings.get(f"{prefix}padding_y", 10))
        _anim_style = self.settings.get(f"{prefix}anim_style", "Slide").lower()
        target_opacity = float(self.settings.get(f"{prefix}opacity", 0.92))
        border_width = int(self.settings.get(f"{prefix}border_width", 0))
        border_color = self.settings.get(f"{prefix}border_color", accent_default)

        target_opacity = max(0.0, min(1.0, target_opacity))
        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = accent_default
        if not border_color or not border_color.startswith("#"):
            border_color = accent_default
        if not emoji:
            emoji = "👁️" if not self.is_health_tip else "💡"
            
        trans_color = "#010203"
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if accent_col == trans_color:
            accent_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"

        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        enable_shadow = self.settings.get(f"{prefix}shadow", True)
        accent_stripe = self.settings.get(f"{prefix}accent_stripe", False)
        text_align = self.settings.get(f"{prefix}text_align", "left")

        shadow_offset = 6 if enable_shadow else 0
        canvas_w = tw + shadow_offset * 2
        canvas_h = th + shadow_offset * 2

        sw = self.toast_window.winfo_screenwidth()
        sh = self.toast_window.winfo_screenheight()
        padding_edge = 20
        fx, fy = 0, 0
        if "top" in pos or pos in ("left", "center", "right"):
            fy = padding_edge
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "bottom" in pos:
            fy = sh - th - 50
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        elif "middle" in pos:
            fy = (sh - th) // 2
            if "left" in pos:
                fx = padding_edge
            elif "right" in pos:
                fx = sw - tw - padding_edge
            else:
                fx = (sw - tw) // 2
        else:
            fx = int(self.settings.get(f"{prefix}custom_x", (sw - tw) // 2))
            fy = int(self.settings.get(f"{prefix}custom_y", padding_edge))

        self.pos = pos
        y_offset = self.slot_index * (th + 10)
        if "bottom" in self.pos:
            fy -= y_offset
        else:
            fy += y_offset

        try:
            self.toast_window.geometry(f"{canvas_w}x{canvas_h}+{fx}+{fy}")
            self.toast_window.attributes("-alpha", target_opacity)
        except tk.TclError:
            pass

        canvas = self.canvas
        canvas.delete("all")
        canvas.configure(width=canvas_w, height=canvas_h)

        def create_round_poly(x, y, w, h, r):
            return [x + r, y, w - r, y, w, y, w, y + r, w, h - r, w, h, w - r, h, x + r, h, x, h, x, h - r, x, y + r, x, y]

        # Shadow
        if enable_shadow:
            shadow_poly = create_round_poly(shadow_offset, shadow_offset, tw + shadow_offset, th + shadow_offset, radius)
            canvas.create_polygon(shadow_poly, smooth=True, fill="#080808")

        # Main background
        bg_poly = create_round_poly(shadow_offset // 2, shadow_offset // 2, tw + shadow_offset // 2, th + shadow_offset // 2, radius)
        
        border_style = self.settings.get(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)
            
        canvas.create_polygon(bg_poly, smooth=True, fill=bg_col, outline=border_color, width=border_width, dash=dash_val)

        # Accent Stripe
        if accent_stripe:
            stripe_pos = self.settings.get(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    tw + shadow_offset // 2 - radius - 4, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + radius,
                    tw + shadow_offset // 2, th + shadow_offset // 2 - radius,
                    tw + shadow_offset // 2 - radius - 4, th + shadow_offset // 2,
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    tw + shadow_offset // 2 - radius, shadow_offset // 2,
                    tw + shadow_offset // 2, shadow_offset // 2 + 4,
                    shadow_offset // 2, shadow_offset // 2 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    shadow_offset // 2 + radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2 - radius, th + shadow_offset // 2 - 4,
                    tw + shadow_offset // 2, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2
                ]
            else: # Left
                stripe_poly = [
                    shadow_offset // 2 + radius, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, shadow_offset // 2,
                    shadow_offset // 2 + radius + 4, th + shadow_offset // 2,
                    shadow_offset // 2 + radius, th + shadow_offset // 2,
                    shadow_offset // 2, th + shadow_offset // 2 - radius,
                    shadow_offset // 2, shadow_offset // 2 + radius
                ]
            canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        msg_font = (font_family, font_size, font_weight)
        sub_font = (font_family, max(8, font_size - 2))

        if msg_font[0] == "Segoe UI" or msg_font[0] == "Segoe UI Emoji":
            msg_font = ("Segoe UI Emoji", msg_font[1], msg_font[2] if len(msg_font) > 2 else "normal")

        anchor = tk.W
        tx = shadow_offset // 2 + padx + 10
        if text_align == "center":
            anchor = tk.CENTER
            tx = shadow_offset // 2 + tw // 2
        elif text_align == "right":
            anchor = tk.E
            tx = shadow_offset // 2 + tw - padx - 10

        show_clock = self.settings.get(f"{prefix}show_clock", False)
        clock_str = f" - {time.strftime('%I:%M %p')}" if show_clock else ""

        if self.is_health_tip:
            canvas.create_text(
                tx, shadow_offset // 2 + th // 2, anchor=anchor,
                text=f"{emoji}  {self.message}{clock_str}", font=msg_font, fill=fg_col,
                width=tw - (padx + 10) * 2,
            )
        else:
            canvas.create_text(
                tx, shadow_offset // 2 + pady, anchor=anchor,
                text=f"{emoji}  {self.title}{clock_str}", font=msg_font, fill=fg_col,
            )
            canvas.create_text(
                tx, shadow_offset // 2 + pady + font_size + 8, anchor=anchor,
                text=self.message, font=sub_font, fill="#8892b0",
                width=tw - (padx + 10) * 2,
            )

    def cleanup(self):
        try:
            # Clear active toast from shared status
            status = read_shared_status()
            if status.get("active_toast_pid") == os.getpid():
                status["active_toast_pid"] = None
                status["active_toast_end_time"] = 0.0
                write_shared_status(status)

            with BaseToast._lock:
                if self in BaseToast._active_toasts:
                    BaseToast._active_toasts.remove(self)
            if self.toast_window:
                self.toast_window.destroy()
        except Exception:
            pass
        finally:
            if not self.settings.get("is_preview", False):
                ToastQueue.on_toast_closed(self.parent)
