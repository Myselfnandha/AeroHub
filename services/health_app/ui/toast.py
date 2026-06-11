import os
import time
import tkinter as tk
from core.logger import logger
from ui.theme import _add_hover

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WarningToast:
    def __init__(self, parent, message: str, duration_sec: int, settings: dict):
        self.parent = parent
        self.message = message
        self.duration = duration_sec
        self.settings = settings
        self.closing = False
        self.window = None

    def show(self):
        try:
            from toast_utils import ToastQueue
            ToastQueue.add(self)
        except Exception:
            self._create_toast()

    def _create_toast(self):
        toast = tk.Toplevel(self.parent)
        self.window = toast
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        trans_color = "#010203"
        toast.configure(bg=trans_color)
        toast.attributes("-transparentcolor", trans_color)
        toast.attributes("-alpha", 0.0)

        # Register in shared status
        from toast_utils import read_shared_status, write_shared_status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        status["active_toast_end_time"] = time.time() + self.duration + 2
        write_shared_status(status)

        tw = int(self.settings.get("toast_width", 260))
        th = int(self.settings.get("toast_height", 60))
        pos = self.settings.get("toast_pos", "Center").lower()
        bg_col = self.settings.get("toast_bg_color", "#252525")
        fg_col = self.settings.get("toast_fg_color", "#ffffff")
        font_size = int(self.settings.get("toast_font_size", 11))
        font_weight = self.settings.get("toast_font_weight", "bold")
        emoji = self.settings.get("toast_emoji", "👁️")
        radius = int(self.settings.get("toast_radius", 16))
        padx = int(self.settings.get("toast_padding_x", 12))
        pady = int(self.settings.get("toast_padding_y", 10))
        anim_style = self.settings.get("toast_anim_style", "Slide").lower()
        opacity = float(self.settings.get("toast_opacity", 0.92))
        border_width = int(self.settings.get("toast_border_width", 0))
        border_color = self.settings.get("toast_border_color", "#7c3aed")

        # Sanitize
        opacity = max(0.0, min(1.0, opacity))
        if bg_col == trans_color:
            bg_col = "#020304"
        if fg_col == trans_color:
            fg_col = "#020304"
        if border_color == trans_color:
            border_color = "#020304"
        padx = min(padx, max(0, tw // 2 - 10))
        pady = min(pady, max(0, th // 2 - 5))

        sw = toast.winfo_screenwidth()
        final_y = 60

        if pos == "left":
            final_x = 20
            start_x, start_y = -tw - 10, final_y
        elif pos == "right":
            final_x = sw - tw - 20
            start_x, start_y = sw + 10, final_y
        else:
            final_x = (sw - tw) // 2
            start_x, start_y = final_x, -th - 10

        if anim_style == "fade":
            toast.geometry(f"{tw}x{th}+{final_x}+{final_y}")
        else:
            toast.geometry(f"{tw}x{th}+{start_x}+{start_y}")

        self.canvas = tk.Canvas(
            toast, width=tw, height=th, bg=trans_color, highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._draw_toast_bg(self.canvas, tw, th, radius, bg_col, border_width, border_color)
        self._draw_toast_text(self.canvas, padx, pady, font_size, font_weight, emoji, fg_col)

        toast.update_idletasks()

        def close_toast(event=None):
            if self.closing:
                return
            self.closing = True
            try:
                from toast_utils import read_shared_status, write_shared_status
                status = read_shared_status()
                if status.get("active_toast_pid") == os.getpid():
                    status["active_toast_pid"] = None
                    status["active_toast_end_time"] = 0.0
                    write_shared_status(status)
            except Exception:
                pass
            try:
                toast.destroy()
            except Exception:
                pass
            try:
                from toast_utils import ToastQueue
                ToastQueue.on_toast_closed(self.parent)
            except Exception:
                pass

        self.force_close = close_toast

        toast.bind("<Button-1>", close_toast)
        self.canvas.bind("<Button-1>", close_toast)
        toast.bind("<ButtonRelease-1>", close_toast)
        self.canvas.bind("<ButtonRelease-1>", close_toast)

        self._animate_in(
            toast,
            tw,
            th,
            start_x,
            start_y,
            final_x,
            final_y,
            anim_style,
            opacity,
            close_toast,
        )
        if self.duration > 0:
            self._play_pre_break_sound()

    def _draw_toast_bg(
        self, canvas, tw, th, radius, bg_col, border_width, border_color
    ):
        points = [
            radius, 0, tw - radius, 0, tw, 0, tw, radius, tw, th - radius, tw, th,
            tw - radius, th, radius, th, 0, th, 0, th - radius, 0, radius, 0, 0
        ]
        if border_width > 0:
            canvas.create_polygon(
                points,
                smooth=True,
                fill=bg_col,
                outline=border_color,
                width=border_width,
            )
        else:
            canvas.create_polygon(points, smooth=True, fill=bg_col)

    def _draw_toast_text(
        self, canvas, padx, pady, font_size, font_weight, emoji, fg_col
    ):
        msg_font = ("Segoe UI", font_size, font_weight)
        sub_font = ("Segoe UI", max(8, font_size - 2))

        canvas.create_text(
            padx + 10,
            pady,
            anchor=tk.NW,
            text=f"{emoji}  {self.message}",
            font=msg_font,
            fill=fg_col,
        )
        self.countdown_text_id = canvas.create_text(
            padx + 10,
            pady + font_size + 8,
            anchor=tk.NW,
            text=f"Break in {self.duration} seconds",
            font=sub_font,
            fill="#8892b0",
        )

    def tick_countdown(self):
        if self.closing:
            return
        if self.duration > 0:
            self.duration -= 1
            try:
                self.canvas.itemconfig(
                    self.countdown_text_id,
                    text=f"Break in {self.duration} seconds"
                )
            except Exception:
                pass
            if self.duration <= 0:
                self.force_close()
            else:
                self.parent.after(1000, self.tick_countdown)

    def _animate_in(self, toast, tw, th, sx, sy, fx, fy, anim_style, opacity, close_cb):
        def slide_in(step=0):
            if self.closing:
                return
            if step <= 20:
                p = step / 20
                ease = 1 - (1 - p) ** 3

                if anim_style == "fade":
                    toast.attributes("-alpha", min(opacity, ease * opacity))
                else:
                    cx = int(sx + (fx - sx) * ease)
                    cy = int(sy + (fy - sy) * ease)
                    try:
                        toast.geometry(f"{tw}x{th}+{cx}+{cy}")
                        toast.attributes("-alpha", min(opacity, ease * opacity))
                    except tk.TclError:
                        pass
                toast.after(16, lambda: slide_in(step + 1))
            else:
                self.tick_countdown()

        slide_in(0)

    def _play_pre_break_sound(self):
        if not self.settings.get("toast_enable_sound", True):
            return
        try:
            import winsound
            sound_path = os.path.join(APP_ROOT, "resources", "on_pre_break.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(
                    sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                )
        except Exception:
            pass



class BrightnessWarningToast:
    def __init__(self, parent, settings, on_skip, on_decrease):
        self.parent = parent
        self.settings = settings
        self.on_skip = on_skip
        self.on_decrease = on_decrease
        self.window = None

    def show(self):
        from toast_utils import is_in_break_period_shared
        if is_in_break_period_shared():
            logger.info("Discarding BrightnessWarningToast because we are in a break period.")
            return
        if self.settings.get("is_preview", False):
            self._create_toast()
            return
        try:
            from toast_utils import ToastQueue
            ToastQueue.add(self)
        except Exception:
            self._create_toast()

    def _create_toast(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Brightness Warning")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)

        trans_color = "#010203"
        self.window.configure(bg=trans_color)
        self.window.attributes("-transparentcolor", trans_color)

        bg_color = self.settings.get("bc_toast_bg_color", "#101625")
        fg_color = self.settings.get("bc_toast_fg_color", "#e2e8f0")
        accent_color = self.settings.get("bc_toast_accent_color", "#ff2a2a")
        emoji = self.settings.get("bc_toast_emoji", "⚠️")
        radius = int(self.settings.get("bc_toast_radius", 16))
        bw = int(self.settings.get("bc_toast_border_width", 1))
        bc = self.settings.get("bc_toast_border_color", "#7c3aed")
        pady = int(self.settings.get("bc_toast_padding_y", 10))

        # Sanitize empty/invalid colors
        if not bg_color or not bg_color.startswith("#"):
            bg_color = "#101625"
        if not fg_color or not fg_color.startswith("#"):
            fg_color = "#e2e8f0"
        if not accent_color or not accent_color.startswith("#"):
            accent_color = "#ff2a2a"
        if not emoji:
            emoji = "⚠️"
        if bg_color == trans_color:
            bg_color = "#020304"
        if fg_color == trans_color:
            fg_color = "#020304"
        if bc == trans_color:
            bc = "#020304"

        pos = self.settings.get("toast_pos", "Center").lower()
        w = int(self.settings.get("bc_toast_width", 320))
        h = int(self.settings.get("bc_toast_height", 145))
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()

        padding = 20
        if "left" in pos:
            x = padding
        elif "right" in pos:
            x = sw - w - padding
        else:
            x = (sw - w) // 2

        if "top" in pos or pos in ("left", "center", "right"):
            y = padding
        elif "bottom" in pos:
            y = sh - h - 50
        else:
            y = padding

        self.window.geometry(f"{w}x{h}+{x}+{y}")

        # Register in shared status
        from toast_utils import read_shared_status, write_shared_status
        status = read_shared_status()
        status["active_toast_pid"] = os.getpid()
        duration = self.settings.get("bc_safe_duration_seconds", 30)
        status["active_toast_end_time"] = time.time() + duration + 2
        write_shared_status(status)

        self.canvas = tk.Canvas(
            self.window, width=w, height=h, bg=trans_color, highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        points = [
            radius, 0, w - radius, 0, w, 0, w, radius, w, h - radius, w, h,
            w - radius, h, radius, h, 0, h, 0, h - radius, 0, radius, 0, 0
        ]
        if bw > 0:
            self.canvas.create_polygon(
                points, smooth=True, fill=bg_color, outline=bc, width=bw
            )
        else:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color)

        # Header text
        self.canvas.create_text(
            w // 2,
            15 + pady,
            anchor=tk.CENTER,
            text=f"{emoji} BRIGHTNESS TOO HIGH",
            font=("Consolas", 12, "bold"),
            fill=accent_color,
        )
        # Subtitle
        self.canvas.create_text(
            w // 2,
            15 + pady + 30,
            anchor=tk.CENTER,
            text="Reduce brightness for eye health?",
            font=("Consolas", 10),
            fill=fg_color,
        )

        # We can place buttons using canvas.create_window
        self._btn_frame = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window(w // 2, 15 + pady + 75, window=self._btn_frame)

        btn_skip = tk.Button(
            self._btn_frame,
            text="SKIP",
            command=self._skip,
            bg="#1a233a",
            fg=fg_color,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=4,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_skip, "#1a233a", bg_color, fg_color, fg_color)

        btn_dec = tk.Button(
            self._btn_frame,
            text="DECREASE",
            command=self._decrease,
            bg=accent_color,
            fg="#070b14",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=4,
        )
        btn_dec.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_dec, accent_color, "#ffffff", "#070b14", "#000000")

        self.window.bind("<Destroy>", self._on_destroy)

        def click_dismiss(event=None):
            if event and event.widget in (self.window, self.canvas):
                self._skip()

        self.window.bind("<Button-1>", click_dismiss)
        self.canvas.bind("<Button-1>", click_dismiss)
        self.window.bind("<ButtonRelease-1>", click_dismiss)
        self.canvas.bind("<ButtonRelease-1>", click_dismiss)

        # Auto-dismiss timer
        if duration > 0:
            self._auto_close_id = self.window.after(int(duration * 1000), self._skip)

        if self.settings.get("bc_toast_enable_sound", True):
            self._play_sound()

    def update_settings(self, settings):
        self.settings = settings
        if not self.window or not self.window.winfo_exists():
            return

        trans_color = "#010203"
        bg_color = self.settings.get("bc_toast_bg_color", "#101625")
        fg_color = self.settings.get("bc_toast_fg_color", "#e2e8f0")
        accent_color = self.settings.get("bc_toast_accent_color", "#ff2a2a")
        emoji = self.settings.get("bc_toast_emoji", "⚠️")
        radius = int(self.settings.get("bc_toast_radius", 16))
        bw = int(self.settings.get("bc_toast_border_width", 1))
        bc = self.settings.get("bc_toast_border_color", "#7c3aed")
        pady = int(self.settings.get("bc_toast_padding_y", 10))

        if not bg_color or not bg_color.startswith("#"):
            bg_color = "#101625"
        if not fg_color or not fg_color.startswith("#"):
            fg_color = "#e2e8f0"
        if not accent_color or not accent_color.startswith("#"):
            accent_color = "#ff2a2a"
        if not emoji:
            emoji = "⚠️"
        if bg_color == trans_color:
            bg_color = "#020304"
        if fg_color == trans_color:
            fg_color = "#020304"
        if bc == trans_color:
            bc = "#020304"

        pos = self.settings.get("toast_pos", "Center").lower()
        w = int(self.settings.get("bc_toast_width", 320))
        h = int(self.settings.get("bc_toast_height", 145))
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()

        padding = 20
        if "left" in pos:
            x = padding
        elif "right" in pos:
            x = sw - w - padding
        else:
            x = (sw - w) // 2

        if "top" in pos or pos in ("left", "center", "right"):
            y = padding
        elif "bottom" in pos:
            y = sh - h - 50
        else:
            y = padding

        try:
            self.window.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

        self.canvas.delete("all")
        self.canvas.configure(width=w, height=h)

        points = [
            radius, 0, w - radius, 0, w, 0, w, radius, w, h - radius, w, h,
            w - radius, h, radius, h, 0, h, 0, h - radius, 0, radius, 0, 0
        ]
        if bw > 0:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color, outline=bc, width=bw)
        else:
            self.canvas.create_polygon(points, smooth=True, fill=bg_color)

        self.canvas.create_text(
            w // 2, 15 + pady, anchor=tk.CENTER,
            text=f"{emoji} BRIGHTNESS TOO HIGH", font=("Consolas", 12, "bold"), fill=accent_color
        )
        self.canvas.create_text(
            w // 2, 15 + pady + 30, anchor=tk.CENTER,
            text="Reduce brightness for eye health?", font=("Consolas", 10), fill=fg_color
        )

        if hasattr(self, "_btn_frame") and self._btn_frame:
            try:
                self._btn_frame.destroy()
            except Exception:
                pass
        self._btn_frame = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window(w // 2, 15 + pady + 75, window=self._btn_frame)

        btn_skip = tk.Button(
            self._btn_frame, text="SKIP", command=self._skip,
            bg="#1a233a", fg=fg_color, relief=tk.FLAT, cursor="hand2", padx=15, pady=4
        )
        btn_skip.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_skip, "#1a233a", bg_color, fg_color, fg_color)

        btn_dec = tk.Button(
            self._btn_frame, text="DECREASE", command=self._decrease,
            bg=accent_color, fg="#070b14", relief=tk.FLAT, cursor="hand2", padx=15, pady=4
        )
        btn_dec.pack(side=tk.LEFT, padx=10)
        _add_hover(btn_dec, accent_color, "#ffffff", "#070b14", "#000000")

    def force_close(self):
        try:
            self.window.destroy()
        except Exception:
            pass

    def _play_sound(self):
        try:
            import winsound

            snd_choice = self.settings.get("bc_toast_sound_effect", "mac_connect")
            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]

            if snd_choice in system_aliases:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
            else:
                if not snd_choice.endswith(".wav"):
                    snd_choice += ".wav"

                path = os.path.join(APP_ROOT, "resources", "sounds", snd_choice)
                if not os.path.exists(path):
                    path = os.path.join(
                        os.path.dirname(APP_ROOT),
                        "BatteryMonitor",
                        "sounds",
                        snd_choice,
                    )

                if os.path.exists(path):
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            logger.error(f"Brightness Warning sound play error: {e}")

    def _skip(self):
        if hasattr(self, "_auto_close_id") and self._auto_close_id:
            try:
                self.window.after_cancel(self._auto_close_id)
            except Exception:
                pass
            self._auto_close_id = None
        if self.on_skip:
            self.on_skip()
        try:
            self.window.destroy()
        except Exception:
            pass

    def _decrease(self):
        if hasattr(self, "_auto_close_id") and self._auto_close_id:
            try:
                self.window.after_cancel(self._auto_close_id)
            except Exception:
                pass
            self._auto_close_id = None
        if self.on_decrease:
            self.on_decrease()
        try:
            self.window.destroy()
        except Exception:
            pass

    def _on_destroy(self, event):
        if event.widget == self.window:
            if hasattr(self, "_auto_close_id") and self._auto_close_id:
                try:
                    self.window.after_cancel(self._auto_close_id)
                except Exception:
                    pass
                self._auto_close_id = None
            try:
                from toast_utils import read_shared_status, write_shared_status
                status = read_shared_status()
                if status.get("active_toast_pid") == os.getpid():
                    status["active_toast_pid"] = None
                    status["active_toast_end_time"] = 0.0
                    write_shared_status(status)
            except Exception:
                pass
            try:
                if not self.settings.get("is_preview", False):
                    from toast_utils import ToastQueue
                    ToastQueue.on_toast_closed(self.parent)
            except Exception:
                pass
