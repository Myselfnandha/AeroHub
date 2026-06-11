import os
import time
import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import ImageTk

from core.logger import logger
from core.constants import TH, DEFAULT_SETTINGS, HEALTH_TIPS, SOUND_EFFECTS
from core.settings import save_settings
from core.gamma import apply_gamma_ramp
from ui.theme import _add_hover, apply_dwm_rounding, create_health_icon
from ui.toast import BrightnessWarningToast
from toast_utils import BaseToast
from core.audio import get_sapi_voices

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SettingsWindow:
    def __init__(self, parent, settings: dict, on_save, app=None):
        self.parent = parent
        self.settings = settings
        self.on_save = on_save
        self.app = app
        self.entries = {}
        self.frames = {}
        self.live_preview_toast = None
        self.live_preview_tab = None

    def show(self):
        self._create()

    def _create(self):
        root = tk.Toplevel(self.parent)
        root.title("SYSTEM OVERRIDE // HEALTH CONFIG")
        root.configure(bg=TH["bg"])
        root.resizable(True, True)
        root.grab_set()

        try:
            icon_img = create_health_icon()
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(False, self.icon_photo)
        except Exception as e:
            logger.error(f"Failed to set window icon: {e}")

        try:
            apply_gamma_ramp(6500, log_action=False)  # Temp reset for configuration clarity
            apply_dwm_rounding(root)
        except Exception:
            pass

        def on_closing():
            if hasattr(self, "live_preview_toast") and self.live_preview_toast:
                try:
                    self.live_preview_toast.force_close()
                except Exception:
                    pass
                self.live_preview_toast = None
                
            for key in list(self.entries.keys()):
                var, var_type = self.entries.pop(key)
                del var

            root.grab_release()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Centered settings window
        root.update_idletasks()
        w = 1000
        h = 700
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(900, 600)

        # Main Layout: Sidebar (Left) and Content (Right)
        main_container = tk.Frame(root, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=210)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Title in Sidebar
        tk.Label(
            self.sidebar,
            text="HEALTH APP",
            font=("Segoe UI", 16, "bold"),
            bg=TH["bg2"],
            fg=TH["fg"],
        ).pack(pady=(32, 20))

        # Content Area
        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frames = {}
        self.nav_buttons = {}
        self.current_frame = None
        self.current_frame_name = None

        self.nav_names = [
            "📅 Schedule",
            "✨ Toast FX",
            "💡 Health Toast",
            "🔆 Brightness Care",
            "🌙 Night Care",
        ]
        self.preview_canvases = {}

        for name in self.nav_names:
            tab_container = tk.Frame(self.content_area, bg=TH["bg"])
            self.frames[name] = tab_container

            if name.endswith("Toast FX") or name.endswith("Health Toast") or name.endswith("Brightness Care") or name.endswith("Night Care"):
                tab_container.columnconfigure(0, weight=3)
                tab_container.columnconfigure(1, weight=2)
                tab_container.rowconfigure(0, weight=1)

                left_container = tk.Frame(tab_container, bg=TH["bg"])
                left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

                scroll_frame = self._create_scrollable_tab(left_container)
                scroll_frame.columnconfigure(0, weight=1)
                scroll_frame.columnconfigure(1, weight=1)

                right_container = tk.Frame(tab_container, bg=TH["bg"])
                right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
                if name.endswith("Health Toast"):
                    self._build_health_previews_container(right_container)
                else:
                    self._build_embedded_preview_panel(right_container, name)
            else:
                tab_container.columnconfigure(0, weight=1)
                tab_container.rowconfigure(0, weight=1)

                left_container = tk.Frame(tab_container, bg=TH["bg"])
                left_container.grid(row=0, column=0, sticky="nsew")

                scroll_frame = self._create_scrollable_tab(left_container)
                scroll_frame.columnconfigure(0, weight=1)
                scroll_frame.columnconfigure(1, weight=1)

            if name.endswith("Schedule"):
                self._build_schedule_tab(scroll_frame)
            elif name.endswith("Toast FX"):
                self._build_toast_tab(scroll_frame)
            elif name.endswith("Health Toast"):
                self._build_health_toast_tab(scroll_frame)
            elif name.endswith("Brightness Care"):
                self._build_brightness_care_tab(scroll_frame)
            elif name.endswith("Night Care"):
                self._build_night_care_tab(scroll_frame)

        def switch_tab(name):
            if hasattr(self, "live_preview_toast") and self.live_preview_toast:
                self._save_silently()
                try:
                    self.live_preview_toast.force_close()
                except Exception:
                    pass
                self.live_preview_toast = None

            if self.current_frame:
                self.current_frame.pack_forget()
                self._style_tab_button(self.current_frame_name, active=False)

            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            self._style_tab_button(name, active=True)
            self._on_settings_modified()

        # Navigation Buttons in Sidebar
        for name in self.nav_names:
            btn = tk.Button(
                self.sidebar,
                text=f"   {name}",
                font=("Segoe UI", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["fg"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

            def bind_tab_hover(b=btn, n=name):
                def on_enter(e):
                    if self.current_frame_name != n:
                        b.config(bg=TH["bg3"], fg=TH["fg"])
                def on_leave(e):
                    if self.current_frame_name != n:
                        b.config(bg=TH["bg2"], fg=TH["fg_dim"])
                b.bind("<Enter>", on_enter)
                b.bind("<Leave>", on_leave)
            bind_tab_hover()

        # Save Button in Sidebar (Bottom)
        btn_save = tk.Button(
            self.sidebar,
            text="Save Settings",
            font=("Segoe UI", 11, "bold"),
            bg=TH["accent"],
            fg="#000000",
            activebackground=TH["accent_hover"],
            activeforeground="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            pady=16,
            command=lambda: self._save_and_close(root),
        )
        btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(10, 20))
        _add_hover(btn_save, TH["accent"], TH["accent_hover"], "#000000", "#000000")

        # Restore Defaults Button in Sidebar (above Save Settings)
        btn_restore = tk.Button(
            self.sidebar,
            text="Restore Defaults",
            font=("Segoe UI", 11, "bold"),
            bg=TH["danger"],
            fg="#ffffff",
            activebackground="#ff6b6b",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            pady=16,
            command=self._restore_defaults,
        )
        btn_restore.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=10)
        _add_hover(btn_restore, TH["danger"], "#ff6b6b", "#ffffff", "#ffffff")

        # Upcoming Break countdown panel in sidebar
        upcoming_frame = tk.Frame(
            self.sidebar,
            bg=TH["bg"],
            highlightthickness=1,
            highlightbackground=TH["border"],
            padx=16,
            pady=16,
        )
        upcoming_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(10, 20))

        self.upcoming_title_label = tk.Label(
            upcoming_frame,
            text="UPCOMING BREAK",
            font=("Segoe UI", 9, "bold"),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor="w",
        )
        self.upcoming_title_label.pack(fill=tk.X, pady=(0, 6))

        self.upcoming_type_label = tk.Label(
            upcoming_frame,
            text="Short Break",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg"],
            fg=TH["accent"],
            anchor="w",
        )
        self.upcoming_type_label.pack(fill=tk.X)

        self.upcoming_time_label = tk.Label(
            upcoming_frame,
            text="00m 00s",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
            anchor="w",
        )
        self.upcoming_time_label.pack(fill=tk.X, pady=4)

        self.upcoming_clock_label = tk.Label(
            upcoming_frame,
            text="at --:--:--",
            font=("Segoe UI", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor="w",
        )
        self.upcoming_clock_label.pack(fill=tk.X)

        self._update_upcoming_break()

        switch_tab("📅 Schedule")

    def _style_tab_button(self, name, active):
        btn = self.nav_buttons[name]
        if active:
            btn.config(bg=TH["bg3"], fg=TH["accent"], text=f"●  {name[2:].strip()}")
        else:
            btn.config(bg=TH["bg2"], fg=TH["fg_dim"], text=f"   {name}")

    def _create_scrollable_tab(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)

        canvas = tk.Canvas(parent, bg=TH["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])

        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        def update_scrollregion(e=None):
            req_w = scrollable_frame.winfo_reqwidth()
            req_h = scrollable_frame.winfo_reqheight()
            canvas.configure(scrollregion=(0, 0, req_w, req_h))

            canvas_h = canvas.winfo_height()
            if req_h > canvas_h and canvas_h > 1:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def _on_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)
            req_h = scrollable_frame.winfo_reqheight()
            if req_h > e.height:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            if scrollbar.winfo_ismapped():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        return scrollable_frame

    def _create_card(self, parent, title, row, col, rowspan=1, columnspan=1):
        card = tk.Frame(
            parent,
            bg=TH["bg2"],
            highlightthickness=1,
            highlightbackground=TH["border"],
            padx=20,
            pady=20,
        )
        card.grid(
            row=row,
            column=col,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
            padx=10,
            pady=10,
        )
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=TH["bg2"],
            fg=TH["fg"],
            anchor=tk.W,
        ).pack(anchor=tk.W, pady=(0, 12))

        content_frame = tk.Frame(card, bg=TH["bg2"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        return card, content_frame

    def _add_field(self, parent_frame, label, key, row, col=0, is_str=False):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=str(self.settings.get(key, "")))
        entry = tk.Entry(
            cell,
            textvariable=var,
            font=("Consolas", 10),
            bg=TH["bg"],
            fg=TH["fg"],
            insertbackground=TH["accent"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=TH["accent"],
            highlightbackground=TH["border"],
            width=14,
        )
        entry.pack(side=tk.RIGHT, padx=(10, 0))

        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return entry

    def _add_combo(self, parent_frame, label, key, row, values, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=self.settings.get(key, values[0]))
        combo = ttk.Combobox(
            cell,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=14,
        )
        combo.pack(side=tk.RIGHT, padx=(10, 0))

        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return combo

    def _add_color_field(self, parent_frame, label, key, row, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        tk.Label(
            cell,
            text=label.upper(),
            font=("Consolas", 9),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            color_code = colorchooser.askcolor(
                title=f"Choose {label}", initialcolor=v.get()
            )[1]
            if color_code:
                v.set(color_code)
                btn.config(bg=color_code)
                self._on_settings_modified()

        btn = tk.Button(
            cell,
            bg=var.get() if var.get() else TH["accent"],
            width=8,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.pack(side=tk.RIGHT, padx=(10, 0))

        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return btn

    def _create_toggle_canvas(self, parent, var):
        cv = tk.Canvas(
            parent, width=44, height=24, bg=parent.cget("bg"), highlightthickness=0
        )

        def draw_toggle(*args):
            cv.delete("all")
            state = var.get()
            color = TH["success"] if state else TH["border"]
            cv.create_oval(2, 2, 22, 22, fill=color, outline=color)
            cv.create_oval(22, 2, 42, 22, fill=color, outline=color)
            cv.create_rectangle(12, 2, 32, 22, fill=color, outline=color)
            if state:
                cv.create_oval(24, 4, 40, 20, fill="#ffffff", outline="#ffffff")
            else:
                cv.create_oval(4, 4, 20, 20, fill="#ffffff", outline="#ffffff")

        draw_toggle()

        def toggle(e=None):
            var.set(not var.get())
            draw_toggle()
            self._on_settings_modified()

        cv.bind("<Button-1>", toggle)
        return cv

    def _add_chk(self, parent, label, key):
        bg = parent.cget("bg")
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill=tk.X, pady=8)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 10),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT)

        var = tk.BooleanVar(value=self.settings.get(key, True))
        self.entries[key] = (var, "bool")

        cv = self._create_toggle_canvas(frame, var)
        cv.pack(side=tk.RIGHT)
        return frame

    def _add_grid_chk(self, parent_frame, label, key, row, col=0):
        bg = parent_frame.cget("bg")
        cell = tk.Frame(parent_frame, bg=bg)
        cell.grid(row=row, column=col, sticky="ew", padx=10, pady=6)
        parent_frame.grid_columnconfigure(col, weight=1)

        var = tk.BooleanVar(value=self.settings.get(key, True))
        self.entries[key] = (var, "bool")

        tk.Label(
            cell,
            text=label,
            font=("Segoe UI", 10),
            bg=bg,
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        cv = self._create_toggle_canvas(cell, var)
        cv.pack(side=tk.RIGHT, padx=(10, 0))
        return cv

    def _build_schedule_tab(self, tab):
        card1, f1 = self._create_card(tab, "Break Times", 0, 0)
        self._add_field(f1, "Short Interval (min):", "short_break_interval_min", 0, col=0)
        self._add_field(f1, "Short Duration (sec):", "short_break_duration_sec", 0, col=1)
        self._add_field(f1, "Long Interval (min):", "long_break_interval_min", 1, col=0)
        self._add_field(f1, "Long Duration (sec):", "long_break_duration_sec", 1, col=1)
        self._add_field(f1, "Pre-warning (sec):", "pre_warning_sec", 2, col=0)

        card2, f2 = self._create_card(tab, "Environment & Astro", 0, 1)
        self._add_field(f2, "Latitude:", "latitude", 0, col=0)
        self._add_field(f2, "Longitude:", "longitude", 0, col=1)
        self._add_field(f2, "Night Start (hr):", "night_light_start_hour", 1, col=0)
        self._add_field(f2, "Night End (hr):", "night_light_end_hour", 1, col=1)
        self._add_field(f2, "Transition (sec):", "nl_transition_duration", 2, col=0)

        card3, f3 = self._create_card(tab, "Audio Source & Options", 1, 0)
        audio_sources = [
            "default", "random", "campfire", "forest", "night", "ocean", "rain", "waterfall"
        ]
        self._add_combo(f3, "Break Audio Source:", "break_audio_source", 0, audio_sources, col=0)

        self._add_grid_chk(f3, "Enable breathing sound", "enable_sound", 1, col=0)
        self._add_grid_chk(f3, "Dim screen during breaks", "enable_dimming", 1, col=1)
        self._add_grid_chk(f3, "Weather color warmth", "enable_weather_warmth", 2, col=0)
        self._add_grid_chk(f3, "Run breaks during games", "run_during_game", 2, col=1)
        self._add_grid_chk(f3, "Enable Night Light", "nl_enabled", 3, col=0)

        card4, f4 = self._create_card(tab, "Box Breathing & Voice Guide", 1, 1)
        self._add_grid_chk(f4, "Enable voice guide", "voice_prompts_enabled", 0, col=0)
        self._add_combo(f4, "Voice Model:", "voice_name", 0, get_sapi_voices(), col=1)
        
        self._add_field(f4, "Inhale (sec):", "voice_inhale_sec", 1, col=0)
        self._add_field(f4, "Hold In (sec):", "voice_hold_in_sec", 1, col=1)
        self._add_field(f4, "Exhale (sec):", "voice_exhale_sec", 2, col=0)
        self._add_field(f4, "Hold Out (sec):", "voice_hold_out_sec", 2, col=1)
        
        self._add_field(f4, "Volume (0-100):", "voice_volume", 3, col=0)
        self._add_field(f4, "Speed Rate:", "voice_rate", 3, col=1)
        
        self._add_combo(f4, "Break Type:", "voice_break_type", 4, ["Both", "Short Only", "Long Only"], col=0)
        self._add_field(f4, "Min Duration (s):", "voice_min_duration_sec", 4, col=1)
        
        self._add_field(f4, "Inhale Text:", "voice_inhale_text", 5, col=0, is_str=True)
        self._add_field(f4, "Exhale Text:", "voice_exhale_text", 5, col=1, is_str=True)
        self._add_field(f4, "Hold In Text:", "voice_hold_in_text", 6, col=0, is_str=True)
        self._add_field(f4, "Hold Out Text:", "voice_hold_out_text", 6, col=1, is_str=True)

    def _build_toast_tab(self, tab):
        card1, f1 = self._create_card(tab, "Layout & Animation", 0, 0, columnspan=2)
        self._add_combo(
            f1, "Position:", "toast_pos", 0, col=0,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )
        self._add_combo(
            f1, "Animation:", "toast_anim_style", 0, col=1,
            values=["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"]
        )
        self._add_field(f1, "Transition Time (ms):", "toast_transition_time_ms", 1, col=0)
        self._add_field(f1, "Display Duration (sec):", "toast_duration_sec", 1, col=1)
        self._add_field(f1, "Width (px):", "toast_width", 2, col=0)
        self._add_field(f1, "Height (px):", "toast_height", 2, col=1)
        self._add_field(f1, "Font Size:", "toast_font_size", 3, col=0)
        self._add_combo(f1, "Font Weight:", "toast_font_weight", 3, ["normal", "bold"], col=1)
        self._add_field(f1, "Emoji Icon:", "toast_emoji", 4, col=0, is_str=True)
        self._add_combo(f1, "Text Align:", "toast_text_align", 4, ["left", "center", "right"], col=1)

        card2, f2 = self._create_card(tab, "Visual Styling", 1, 0, columnspan=2)
        self._add_color_field(f2, "Background Color:", "toast_bg_color", 0, col=0)
        self._add_color_field(f2, "Text Color:", "toast_fg_color", 0, col=1)
        self._add_color_field(f2, "Accent Color:", "toast_accent_color", 1, col=0)
        self._add_color_field(f2, "Gradient End:", "toast_gradient_end", 1, col=1)
        self._add_field(f2, "Border Radius (px):", "toast_radius", 2, col=0)
        self._add_field(f2, "Border Width (px):", "toast_border_width", 2, col=1)
        self._add_color_field(f2, "Border Color:", "toast_border_color", 3, col=0)
        self._add_combo(f2, "Border Style:", "toast_border_style", 3, ["Solid", "Dashed", "Dotted"], col=1)
        self._add_combo(f2, "Stripe Position:", "toast_stripe_pos", 4, ["Left", "Right", "Top", "Bottom"], col=0)
        self._add_field(f2, "Opacity (0.1 - 1.0):", "toast_opacity", 4, col=1)
        self._add_grid_chk(f2, "Enable Gradient", "toast_gradient", 5, col=0)
        self._add_grid_chk(f2, "Enable Shadow", "toast_shadow", 5, col=1)
        self._add_grid_chk(f2, "Accent Stripe", "toast_accent_stripe", 6, col=0)
        self._add_grid_chk(f2, "Progress Bar", "toast_progress_bar", 6, col=1)
        self._add_field(f2, "Padding X (px):", "toast_padding_x", 7, col=0)
        self._add_field(f2, "Padding Y (px):", "toast_padding_y", 7, col=1)

        card3, f3 = self._create_card(tab, "Audio & Interaction", 2, 0, columnspan=2)
        self._add_grid_chk(f3, "Play Warning Sound", "toast_enable_sound", 0, col=0)
        self._add_combo(f3, "Sound Effect:", "toast_sound_effect", 0, SOUND_EFFECTS, col=1)
        self._add_field(f3, "Volume (0-100):", "toast_volume", 1, col=0)
        self._add_combo(f3, "Click Action:", "toast_click_action", 1, ["dismiss", "snooze", "settings"], col=1)

    def _build_health_toast_tab(self, tab):
        card1, f1 = self._create_card(tab, "Scheduling & Animation", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Health Tips", "ht_enabled", 0, col=0)
        self._add_field(f1, "Interval (min):", "ht_interval_min", 0, col=1)
        self._add_field(f1, "Display Duration (sec):", "ht_duration_sec", 1, col=0)
        self._add_field(f1, "Transition Time (ms):", "ht_toast_transition_time_ms", 1, col=1)
        self._add_combo(
            f1, "Position:", "ht_toast_pos", 2, col=0,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )
        self._add_combo(
            f1, "Animation:", "ht_toast_anim_style", 2, col=1,
            values=["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"]
        )

        card2, f2 = self._create_card(tab, "Tip Categories", 1, 0, columnspan=2)
        self._add_grid_chk(f2, "Breathing Exercises", "ht_cat_breathing", 0, col=0)
        self._add_grid_chk(f2, "Eye Care Tips", "ht_cat_eye_care", 0, col=1)
        self._add_grid_chk(f2, "Posture Adjustment", "ht_cat_posture", 1, col=0)
        self._add_grid_chk(f2, "Muscle Stretching", "ht_cat_stretch", 1, col=1)
        self._add_grid_chk(f2, "Hydration Reminders", "ht_cat_hydration", 2, col=0)
        self._add_grid_chk(f2, "Mental Ease Moments", "ht_cat_mental", 2, col=1)
        self._add_grid_chk(f2, "Hands & Wrists", "ht_cat_hands_wrists", 3, col=0)

        card3, f3 = self._create_card(tab, "Toast Style & Audio", 2, 0, columnspan=2)
        self._add_field(f3, "Width (px):", "ht_toast_width", 0, col=0)
        self._add_field(f3, "Height (px):", "ht_toast_height", 0, col=1)
        self._add_color_field(f3, "Background Color:", "ht_toast_bg_color", 1, col=0)
        self._add_color_field(f3, "Text Color:", "ht_toast_fg_color", 1, col=1)
        self._add_color_field(f3, "Accent Color:", "ht_toast_accent_color", 2, col=0)
        self._add_color_field(f3, "Gradient End:", "ht_toast_gradient_end", 2, col=1)
        self._add_field(f3, "Font Size:", "ht_toast_font_size", 3, col=0)
        self._add_field(f3, "Border Radius (px):", "ht_toast_radius", 3, col=1)
        self._add_field(f3, "Border Width (px):", "ht_toast_border_width", 4, col=0)
        self._add_color_field(f3, "Border Color:", "ht_toast_border_color", 4, col=1)
        self._add_combo(f3, "Border Style:", "ht_toast_border_style", 5, ["Solid", "Dashed", "Dotted"], col=0)
        self._add_combo(f3, "Stripe Position:", "ht_toast_stripe_pos", 5, ["Left", "Right", "Top", "Bottom"], col=1)
        self._add_field(f3, "Opacity (0.1 - 1.0):", "ht_toast_opacity", 6, col=0)
        self._add_combo(f3, "Text Align:", "ht_toast_text_align", 6, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "ht_toast_gradient", 7, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "ht_toast_shadow", 7, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "ht_toast_accent_stripe", 8, col=0)
        self._add_grid_chk(f3, "Progress Bar", "ht_toast_progress_bar", 8, col=1)
        self._add_grid_chk(f3, "Play Tip Sound", "ht_toast_enable_sound", 9, col=0)
        self._add_combo(f3, "Sound Effect:", "ht_toast_sound_effect", 9, SOUND_EFFECTS, col=1)
        self._add_field(f3, "Volume (0-100):", "ht_toast_volume", 10, col=0)
        self._add_combo(f3, "Click Action:", "ht_toast_click_action", 10, ["dismiss", "snooze", "settings"], col=1)
        self._add_field(f3, "Padding X (px):", "ht_toast_padding_x", 11, col=0)
        self._add_field(f3, "Padding Y (px):", "ht_toast_padding_y", 11, col=1)

    def _build_brightness_care_tab(self, tab):
        card1, f1 = self._create_card(tab, "Auto Dimming Scheduler", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Brightness Care", "bc_enabled", 0, col=0)
        self._add_field(f1, "Start Time (HH:MM):", "bc_start_time", 0, col=1, is_str=True)
        self._add_field(f1, "End Time (HH:MM):", "bc_end_time", 1, col=0, is_str=True)
        self._add_field(f1, "Target Brightness (%):", "bc_target_brightness", 1, col=1)
        self._add_field(f1, "Transition Duration (min):", "bc_duration_minutes", 2, col=0)
        self._add_field(f1, "Normal Fade (sec):", "bc_transition_time_sec", 2, col=1)

        card2, f2 = self._create_card(tab, "Aggressive & Safe Limits", 1, 0, columnspan=2)
        self._add_field(f2, "Aggressive Target (%):", "bc_aggressive_target_brightness", 0, col=0)
        self._add_field(f2, "Aggressive Duration (min):", "bc_aggressive_duration_minutes", 0, col=1)
        self._add_field(f2, "Aggressive Fade (sec):", "bc_aggressive_transition_time_sec", 1, col=0)
        self._add_field(f2, "Safe Brightness (%):", "bc_safe_brightness", 2, col=0)
        self._add_field(f2, "Safe Duration (sec):", "bc_safe_duration_seconds", 2, col=1)

        card3, f3 = self._create_card(tab, "Toast Visuals & Audio", 2, 0, columnspan=2)
        self._add_field(f3, "Display Duration (sec):", "bc_toast_duration_sec", 0, col=0)
        self._add_field(f3, "Transition Time (ms):", "bc_toast_transition_time_ms", 0, col=1)
        self._add_combo(f3, "Animation Style:", "bc_toast_anim_style", 1, ["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"], col=0)
        self._add_combo(f3, "Position:", "bc_toast_pos", 1, ["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"], col=1)
        self._add_field(f3, "Width (px):", "bc_toast_width", 2, col=0)
        self._add_field(f3, "Height (px):", "bc_toast_height", 2, col=1)
        self._add_color_field(f3, "Background Color:", "bc_toast_bg_color", 3, col=0)
        self._add_color_field(f3, "Text Color:", "bc_toast_fg_color", 3, col=1)
        self._add_color_field(f3, "Accent Color:", "bc_toast_accent_color", 4, col=0)
        self._add_color_field(f3, "Gradient End:", "bc_toast_gradient_end", 4, col=1)
        self._add_field(f3, "Emoji Icon:", "bc_toast_emoji", 5, col=0, is_str=True)
        self._add_field(f3, "Border Radius (px):", "bc_toast_radius", 5, col=1)
        self._add_field(f3, "Border Width (px):", "bc_toast_border_width", 6, col=0)
        self._add_color_field(f3, "Border Color:", "bc_toast_border_color", 6, col=1)
        self._add_combo(f3, "Border Style:", "bc_toast_border_style", 7, ["Solid", "Dashed", "Dotted"], col=0)
        self._add_combo(f3, "Stripe Position:", "bc_toast_stripe_pos", 7, ["Left", "Right", "Top", "Bottom"], col=1)
        self._add_field(f3, "Opacity (0.1 - 1.0):", "bc_toast_opacity", 8, col=0)
        self._add_combo(f3, "Text Align:", "bc_toast_text_align", 8, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "bc_toast_gradient", 9, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "bc_toast_shadow", 9, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "bc_toast_accent_stripe", 10, col=0)
        self._add_grid_chk(f3, "Progress Bar", "bc_toast_progress_bar", 10, col=1)
        self._add_grid_chk(f3, "Play Warning Sound", "bc_toast_enable_sound", 11, col=0)
        self._add_combo(f3, "Sound Effect:", "bc_toast_sound_effect", 11, SOUND_EFFECTS, col=1)
        self._add_field(f3, "Volume (0-100):", "bc_toast_volume", 12, col=0)
        self._add_combo(f3, "Click Action:", "bc_toast_click_action", 12, ["dismiss", "snooze", "settings"], col=1)
        self._add_field(f3, "Padding X (px):", "bc_toast_padding_x", 13, col=0)
        self._add_field(f3, "Padding Y (px):", "bc_toast_padding_y", 13, col=1)

    def _build_night_care_tab(self, tab):
        card1, f1 = self._create_card(tab, "Late Night Caution", 0, 0, columnspan=2)
        self._add_grid_chk(f1, "Enable Night Care", "nc_enabled", 0, col=0)
        self._add_field(f1, "Start Time (HH:MM):", "nc_start_time", 0, col=1, is_str=True)
        self._add_field(f1, "End Time (HH:MM):", "nc_end_time", 1, col=0, is_str=True)
        self._add_field(f1, "Check Interval (min):", "nc_interval_minutes", 1, col=1)
        self._add_field(f1, "Slogans (pipe-separated):", "nc_slogans", 2, col=0, is_str=True)

        card2, f2 = self._create_card(tab, "Toast Visuals & Audio", 1, 0, columnspan=2)
        self._add_field(f2, "Display Duration (sec):", "nc_toast_duration_sec", 0, col=0)
        self._add_field(f2, "Transition Time (ms):", "nc_toast_transition_time_ms", 0, col=1)
        self._add_combo(f2, "Animation Style:", "nc_toast_anim_style", 1, ["Slide", "Fade", "Bounce", "Scale", "Glow", "Drop", "Typewriter"], col=0)
        self._add_combo(f2, "Position:", "nc_toast_pos", 1, ["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"], col=1)
        self._add_field(f2, "Width (px):", "nc_toast_width", 2, col=0)
        self._add_field(f2, "Height (px):", "nc_toast_height", 2, col=1)
        self._add_color_field(f2, "Background Color:", "nc_toast_bg_color", 3, col=0)
        self._add_color_field(f2, "Text Color:", "nc_toast_fg_color", 3, col=1)
        self._add_color_field(f2, "Accent Color:", "nc_toast_accent_color", 4, col=0)
        self._add_color_field(f2, "Gradient End:", "nc_toast_gradient_end", 4, col=1)
        self._add_field(f2, "Font Size:", "nc_toast_font_size", 5, col=0)
        self._add_field(f2, "Emoji Icon:", "nc_toast_emoji", 5, col=1, is_str=True)
        self._add_field(f2, "Border Radius (px):", "nc_toast_radius", 6, col=0)
        self._add_field(f2, "Border Width (px):", "nc_toast_border_width", 6, col=1)
        self._add_color_field(f2, "Border Color:", "nc_toast_border_color", 7, col=0)
        self._add_combo(f2, "Border Style:", "nc_toast_border_style", 7, ["Solid", "Dashed", "Dotted"], col=1)
        self._add_combo(f2, "Stripe Position:", "nc_toast_stripe_pos", 8, ["Left", "Right", "Top", "Bottom"], col=0)
        self._add_field(f2, "Opacity (0.1 - 1.0):", "nc_toast_opacity", 8, col=1)
        self._add_combo(f2, "Text Align:", "nc_toast_text_align", 9, ["left", "center", "right"], col=0)
        self._add_grid_chk(f2, "Enable Gradient", "nc_toast_gradient", 9, col=1)
        self._add_grid_chk(f2, "Enable Shadow", "nc_toast_shadow", 10, col=0)
        self._add_grid_chk(f2, "Accent Stripe", "nc_toast_accent_stripe", 10, col=1)
        self._add_grid_chk(f2, "Progress Bar", "nc_toast_progress_bar", 11, col=0)
        self._add_grid_chk(f2, "Play Warning Sound", "nc_toast_enable_sound", 11, col=1)
        self._add_combo(f2, "Sound Effect:", "nc_toast_sound_effect", 12, SOUND_EFFECTS, col=0)
        self._add_field(f2, "Volume (0-100):", "nc_toast_volume", 12, col=1)
        self._add_combo(f2, "Click Action:", "nc_toast_click_action", 13, ["dismiss", "snooze", "settings"], col=0)
        self._add_field(f2, "Padding X (px):", "nc_toast_padding_x", 13, col=1)
        self._add_field(f2, "Padding Y (px):", "nc_toast_padding_y", 14, col=0)

    def _build_embedded_preview_panel(self, container, tab_name):
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        card, f = self._create_card(container, f"{tab_name} Preview", 0, 0)

        canvas = tk.Canvas(
            f,
            width=340,
            height=180,
            bg=TH["bg"],
            highlightthickness=1,
            highlightbackground=TH["border"],
        )
        canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.preview_canvases[tab_name] = canvas

        btn_sound = tk.Button(
            f,
            text="[ TEST SOUND ]",
            font=("Consolas", 10, "bold"),
            bg=TH["bg3"],
            fg=TH["accent"],
            activebackground=TH["bg2"],
            activeforeground=TH["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self._test_preview_sound_for_tab(tab_name),
        )
        btn_sound.pack(fill=tk.X, pady=4)
        _add_hover(btn_sound, TH["bg3"], TH["bg2"], TH["accent"], TH["accent"])

        btn_desktop = tk.Button(
            f,
            text="[ SHOW ON DESKTOP ]",
            font=("Consolas", 10, "bold"),
            bg=TH["accent"],
            fg=TH["bg"],
            activebackground=TH["accent_hover"],
            activeforeground=TH["bg"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self._show_desktop_preview_for_tab(tab_name),
        )
        btn_desktop.pack(fill=tk.X, pady=4)
        _add_hover(btn_desktop, TH["accent"], TH["accent_hover"], TH["bg"], TH["bg"])

        canvas.bind("<Configure>", lambda e: self._update_preview_canvas(tab_name))

    def _build_health_previews_container(self, parent):
        # Create a scrollable container inside parent
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)

        canvas = tk.Canvas(parent, bg=TH["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=TH["bg"])

        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        def update_health_scrollregion(e=None):
            req_w = scrollable_frame.winfo_reqwidth()
            req_h = scrollable_frame.winfo_reqheight()
            canvas.configure(scrollregion=(0, 0, req_w, req_h))

            canvas_h = canvas.winfo_height()
            if req_h > canvas_h and canvas_h > 1:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        scrollable_frame.bind("<Configure>", update_health_scrollregion)

        def _on_health_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)
            req_h = scrollable_frame.winfo_reqheight()
            if req_h > e.height:
                scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                scrollbar.grid_remove()

        canvas.bind("<Configure>", _on_health_canvas_configure)

        def _on_mousewheel(event):
            if scrollbar.winfo_ismapped():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        self.health_preview_scroll_frame = scrollable_frame
        self.health_preview_scroll_canvas = canvas
        self.health_preview_canvases = {}
        
        self._rebuild_health_toast_previews()

    def _rebuild_health_toast_previews(self):
        for child in self.health_preview_scroll_frame.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass

        self.health_preview_canvases = {}

        categories = [
            ("ht_cat_breathing", "breathing", "Breathing Exercise"),
            ("ht_cat_eye_care", "eye_care", "Eye Care Tip"),
            ("ht_cat_posture", "posture", "Posture Adjustment"),
            ("ht_cat_stretch", "stretch", "Muscle Stretch"),
            ("ht_cat_hydration", "hydration", "Hydration Reminder"),
            ("ht_cat_mental", "mental", "Mental Ease Moment"),
            ("ht_cat_hands_wrists", "hands_wrists", "Hands & Wrists"),
        ]

        for key, cat_name, label_title in categories:
            is_enabled = False
            if key in self.entries:
                is_enabled = self.entries[key][0].get() in ("1", "True", True)
            else:
                is_enabled = self.settings.get(key, True)

            if is_enabled:
                card_frame = tk.Frame(
                    self.health_preview_scroll_frame,
                    bg=TH["bg2"],
                    highlightthickness=1,
                    highlightbackground=TH["border"],
                    padx=12,
                    pady=12,
                )
                card_frame.pack(fill=tk.X, pady=8, padx=10)

                tk.Label(
                    card_frame,
                    text=label_title.upper(),
                    font=("Segoe UI", 9, "bold"),
                    bg=TH["bg2"],
                    fg=TH["accent"],
                    anchor="w"
                ).pack(anchor="w", pady=(0, 6))

                canvas = tk.Canvas(
                    card_frame,
                    width=300,
                    height=90,
                    bg=TH["bg"],
                    highlightthickness=1,
                    highlightbackground=TH["border"],
                )
                canvas.pack(fill=tk.X, pady=(0, 8))
                self.health_preview_canvases[cat_name] = canvas

                # Bind dynamic redraw
                canvas.bind("<Configure>", lambda e, cn=cat_name: self._update_health_category_preview(cn))

                btn_frame = tk.Frame(card_frame, bg=TH["bg2"])
                btn_frame.pack(fill=tk.X)

                btn_sound = tk.Button(
                    btn_frame,
                    text="TEST SOUND",
                    font=("Consolas", 8, "bold"),
                    bg=TH["bg3"],
                    fg=TH["accent"],
                    activebackground=TH["bg2"],
                    activeforeground=TH["accent"],
                    relief=tk.FLAT,
                    cursor="hand2",
                    padx=8,
                    pady=4,
                    command=lambda cn=cat_name: self._test_health_preview_sound(cn),
                )
                btn_sound.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
                _add_hover(btn_sound, TH["bg3"], TH["bg2"], TH["accent"], TH["accent"])

                btn_desktop = tk.Button(
                    btn_frame,
                    text="SHOW ON DESKTOP",
                    font=("Consolas", 8, "bold"),
                    bg=TH["accent"],
                    fg=TH["bg"],
                    activebackground=TH["accent_hover"],
                    activeforeground=TH["bg"],
                    relief=tk.FLAT,
                    cursor="hand2",
                    padx=8,
                    pady=4,
                    command=lambda cn=cat_name: self._show_health_desktop_preview(cn),
                )
                btn_desktop.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))
                _add_hover(btn_desktop, TH["accent"], TH["accent_hover"], TH["bg"], TH["bg"])

                self._update_health_category_preview(cat_name)

    def _update_health_category_preview(self, cat_name):
        canvas = self.health_preview_canvases.get(cat_name)
        if not canvas:
            return
        canvas.delete("all")

        prefix = "ht_toast_"
        message = HEALTH_TIPS[cat_name][0]

        def get_val(key, default):
            if key in self.entries:
                return self.entries[key][0].get()
            return self.settings.get(key, default)

        try:
            tw = int(get_val(f"{prefix}width", 280))
        except ValueError:
            tw = 280
        try:
            th = int(get_val(f"{prefix}height", 70))
        except ValueError:
            th = 70
        bg_col = get_val(f"{prefix}bg_color", "#252525")
        fg_col = get_val(f"{prefix}fg_color", "#ffffff")
        accent_col = get_val(f"{prefix}accent_color", "#00f0ff")
        try:
            font_size = int(get_val(f"{prefix}font_size", 11))
        except ValueError:
            font_size = 11
        font_weight = get_val(f"{prefix}font_weight", "bold")
        font_family = get_val(f"{prefix}font_family", "Segoe UI")
        emoji = get_val(f"{prefix}emoji", "💡")
        try:
            radius = int(get_val(f"{prefix}radius", 16))
        except ValueError:
            radius = 16
        try:
            border_width = int(get_val(f"{prefix}border_width", 0))
        except ValueError:
            border_width = 0
        border_color = get_val(f"{prefix}border_color", "#00f0ff")
        try:
            padx = int(get_val(f"{prefix}padding_x", 12))
        except ValueError:
            padx = 12

        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = "#00f0ff"
        if not border_color or not border_color.startswith("#"):
            border_color = "#00f0ff"
        if not emoji:
            emoji = "💡"

        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 10:
            cw = 300
        if ch < 10:
            ch = 90

        scale = 1.0
        if th > 0:
            original_ratio = tw / th
        else:
            original_ratio = 1.0

        max_target_w = cw - 20
        max_target_h = ch - 20

        if max_target_w <= 0:
            max_target_w = 280
        if max_target_h <= 0:
            max_target_h = 70

        if max_target_w / original_ratio <= max_target_h:
            scaled_w = max_target_w
            scaled_h = int(max_target_w / original_ratio)
        else:
            scaled_h = max_target_h
            scaled_w = int(max_target_h * original_ratio)

        if tw > 0:
            scale = scaled_w / tw
        else:
            scale = 1.0

        scaled_r = int(radius * scale)
        scaled_bw = int(border_width * scale)

        x1 = (cw - scaled_w) // 2
        y1 = (ch - scaled_h) // 2
        x2 = x1 + scaled_w
        y2 = y1 + scaled_h

        def get_rounded_points(x, y, w, h, r):
            return [x + r, y, w - r, y, w, y, w, y + r, w, h - r, w, h, w - r, h, x + r, h, x, h, x, h - r, x, y + r, x, y]

        points = get_rounded_points(x1, y1, x2, y2, scaled_r)
        
        border_style = get_val(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)

        canvas.create_polygon(
            points,
            smooth=True,
            fill=bg_col,
            outline=border_color if border_width > 0 else "",
            width=scaled_bw if border_width > 0 else 0,
            dash=dash_val
        )

        accent_stripe = False
        stripe_key = f"{prefix}accent_stripe"
        if stripe_key in self.entries:
            val = self.entries[stripe_key][0].get()
            accent_stripe = val == "1" or val == "True" or val is True
        else:
            accent_stripe = self.settings.get(stripe_key, False)

        if accent_stripe:
            stripe_pos = get_val(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    x2 - scaled_r - 4, y1,
                    x2, y1 + scaled_r,
                    x2, y2 - scaled_r,
                    x2 - scaled_r - 4, y2
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    x1 + scaled_r, y1,
                    x2 - scaled_r, y1,
                    x2, y1 + 4,
                    x1, y1 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    x1 + scaled_r, y2 - 4,
                    x2 - scaled_r, y2 - 4,
                    x2, y2,
                    x1, y2
                ]
            else: # Left
                stripe_poly = [
                    x1 + scaled_r, y1,
                    x1 + scaled_r + 4, y1,
                    x1 + scaled_r + 4, y2,
                    x1 + scaled_r, y2,
                    x1, y2 - scaled_r,
                    x1, y1 + scaled_r
                ]
            canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        msg_font = (font_family, int(font_size * scale), font_weight)

        align_key = f"{prefix}text_align"
        if align_key in self.entries:
            text_align = self.entries[align_key][0].get()
        else:
            text_align = self.settings.get(align_key, "left")

        anchor = tk.W
        tx = x1 + int((padx + 10) * scale)
        if text_align == "center":
            anchor = tk.CENTER
            tx = x1 + scaled_w // 2
        elif text_align == "right":
            anchor = tk.E
            tx = x2 - int((padx + 10) * scale)

        canvas.create_text(
            tx,
            y1 + scaled_h // 2,
            anchor=anchor,
            text=f"{emoji}  {message}",
            font=msg_font,
            fill=fg_col,
            width=scaled_w - int((padx + 10) * 2 * scale),
        )

    def _test_health_preview_sound(self, cat_name):
        self._test_preview_sound_for_tab("💡 Health Toast")

    def _show_health_desktop_preview(self, cat_name):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        temp_settings = dict(self.settings)
        temp_settings["is_preview"] = True
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                ):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        temp_settings["ht_toast_auto_dismiss"] = False
        temp_settings["ht_toast_enable_sound"] = False
        toast = BaseToast(
            self.parent,
            f"HEALTH TIP: {cat_name.replace('_', ' ').upper()}",
            HEALTH_TIPS[cat_name][0],
            temp_settings,
            is_health_tip=True,
        )
        toast.show()
        self.live_preview_toast = toast

    def _get_toast_type_for_tab(self, tab_name):
        if tab_name.endswith("Toast FX"):
            return "General Warning"
        elif tab_name.endswith("Health Toast"):
            return "Health Tip"
        elif tab_name.endswith("Brightness Care"):
            return "Brightness Care"
        elif tab_name.endswith("Night Care"):
            return "Night Care"
        return None

    def _on_settings_modified(self):
        for name in self.preview_canvases:
            self._update_preview_canvas(name)

        if hasattr(self, "health_preview_scroll_frame"):
            enabled_cats = []
            categories = [
                ("ht_cat_breathing", "breathing"),
                ("ht_cat_eye_care", "eye_care"),
                ("ht_cat_posture", "posture"),
                ("ht_cat_stretch", "stretch"),
                ("ht_cat_hydration", "hydration"),
                ("ht_cat_mental", "mental"),
                ("ht_cat_hands_wrists", "hands_wrists"),
            ]
            for key, cat_name in categories:
                is_enabled = False
                if key in self.entries:
                    is_enabled = self.entries[key][0].get() in ("1", "True", True)
                else:
                    is_enabled = self.settings.get(key, True)
                if is_enabled:
                    enabled_cats.append(cat_name)

            current_cats = list(self.health_preview_canvases.keys())
            if set(enabled_cats) != set(current_cats):
                self._rebuild_health_toast_previews()
            else:
                for cat_name in self.health_preview_canvases:
                    self._update_health_category_preview(cat_name)

        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            temp_settings = dict(self.settings)
            for key, (var, var_type) in self.entries.items():
                val = var.get()
                try:
                    if var_type == "bool":
                        temp_settings[key] = val == "1" or val == "True" or val is True
                    elif key in (
                        "latitude",
                        "longitude",
                        "toast_opacity",
                        "ht_toast_opacity",
                        "nc_toast_opacity",
                    ):
                        temp_settings[key] = float(val)
                    elif var_type is False:
                        temp_settings[key] = int(val)
                    else:
                        temp_settings[key] = val
                except ValueError:
                    pass

            toast_type = self._get_toast_type_for_tab(self.current_frame_name)
            if toast_type == "Night Care":
                for k, v in list(temp_settings.items()):
                    if k.startswith("nc_toast_"):
                        suffix = k[len("nc_toast_"):]
                        temp_settings[f"toast_{suffix}"] = v
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "General Warning":
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
            elif toast_type == "Health Tip":
                temp_settings["ht_toast_auto_dismiss"] = False
                temp_settings["ht_toast_enable_sound"] = False
            elif toast_type == "Brightness Care":
                temp_settings["bc_safe_duration_seconds"] = 999999
                temp_settings["bc_toast_enable_sound"] = False

            try:
                self.live_preview_toast.update_settings(temp_settings)
            except Exception as e:
                logger.error(f"Error updating live preview: {e}")

    def _update_preview_canvas(self, tab_name):
        canvas = self.preview_canvases.get(tab_name)
        if not canvas:
            return
        canvas.delete("all")
        toast_type = self._get_toast_type_for_tab(tab_name)
        if not toast_type:
            return

        if toast_type == "General Warning":
            prefix = "toast_"
            title = "EYE BREAK"
            message = "Time to take a break!"
        elif toast_type == "Health Tip":
            prefix = "ht_toast_"
            title = "HEALTH TIP"
            message = "Take a slow, deep breath. Inhale for 4s."
        elif toast_type == "Brightness Care":
            prefix = "bc_toast_"
            emoji = self.entries.get("bc_toast_emoji", [None])[0]
            emoji_val = emoji.get() if emoji else "⚠️"
            title = f"{emoji_val} BRIGHTNESS TOO HIGH"
            message = "Reduce brightness for eye health?"
        else:  # Night Care
            prefix = "nc_toast_"
            title = "NIGHT CARE"
            message = "It's late. Your body needs rest. 🌙"

        def get_val(key, default):
            if key in self.entries:
                return self.entries[key][0].get()
            return self.settings.get(key, default)

        try:
            tw = int(get_val(f"{prefix}width", 260))
        except ValueError:
            tw = 260
        try:
            th = int(get_val(f"{prefix}height", 60))
        except ValueError:
            th = 60
        bg_col = get_val(f"{prefix}bg_color", "#252525")
        fg_col = get_val(f"{prefix}fg_color", "#ffffff")
        accent_col = get_val(f"{prefix}accent_color", "#00f0ff")
        try:
            font_size = int(get_val(f"{prefix}font_size", 11))
        except ValueError:
            font_size = 11
        font_weight = get_val(f"{prefix}font_weight", "bold")
        font_family = get_val(f"{prefix}font_family", "Segoe UI")
        emoji = get_val(f"{prefix}emoji", "👁️")
        try:
            radius = int(get_val(f"{prefix}radius", 16))
        except ValueError:
            radius = 16
        try:
            border_width = int(get_val(f"{prefix}border_width", 0))
        except ValueError:
            border_width = 0
        border_color = get_val(f"{prefix}border_color", "#00f0ff")
        try:
            padx = int(get_val(f"{prefix}padding_x", 12))
        except ValueError:
            padx = 12
        try:
            pady = int(get_val(f"{prefix}padding_y", 10))
        except ValueError:
            pady = 10

        if not bg_col or not bg_col.startswith("#"):
            bg_col = "#252525"
        if not fg_col or not fg_col.startswith("#"):
            fg_col = "#ffffff"
        accent_default = "#00f0ff" if prefix in ("toast_", "ht_toast_") else "#7c3aed"
        if not accent_col or not accent_col.startswith("#"):
            accent_col = accent_default
        if not border_color or not border_color.startswith("#"):
            border_color = accent_default
        if not emoji:
            emoji = "👁️" if prefix == "toast_" else "💡"

        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 10:
            cw = 340
        if ch < 10:
            ch = 180

        scale = 1.0
        if th > 0:
            original_ratio = tw / th
        else:
            original_ratio = 1.0

        max_target_w = cw - 40
        max_target_h = ch - 40

        if max_target_w <= 0:
            max_target_w = 300
        if max_target_h <= 0:
            max_target_h = 140

        if max_target_w / original_ratio <= max_target_h:
            scaled_w = max_target_w
            scaled_h = int(max_target_w / original_ratio)
        else:
            scaled_h = max_target_h
            scaled_w = int(max_target_h * original_ratio)

        if tw > 0:
            scale = scaled_w / tw
        else:
            scale = 1.0

        scaled_r = int(radius * scale)
        scaled_bw = int(border_width * scale)

        x1 = (cw - scaled_w) // 2
        y1 = (ch - scaled_h) // 2
        x2 = x1 + scaled_w
        y2 = y1 + scaled_h

        def get_rounded_points(x, y, w, h, r):
            return [x + r, y, w - r, y, w, y, w, y + r, w, h - r, w, h, w - r, h, x + r, h, x, h, x, h - r, x, y + r, x, y]

        points = get_rounded_points(x1, y1, x2, y2, scaled_r)
        
        border_style = get_val(f"{prefix}border_style", "Solid")
        dash_val = ()
        if border_style == "Dashed":
            dash_val = (6, 4)
        elif border_style == "Dotted":
            dash_val = (2, 2)

        canvas.create_polygon(
            points,
            smooth=True,
            fill=bg_col,
            outline=border_color if border_width > 0 else "",
            width=scaled_bw if border_width > 0 else 0,
            dash=dash_val
        )

        accent_stripe = False
        stripe_key = f"{prefix}accent_stripe"
        if stripe_key in self.entries:
            val = self.entries[stripe_key][0].get()
            accent_stripe = val == "1" or val == "True" or val is True
        else:
            accent_stripe = self.settings.get(stripe_key, False)

        if accent_stripe:
            stripe_pos = get_val(f"{prefix}stripe_pos", "Left")
            if stripe_pos == "Right":
                stripe_poly = [
                    x2 - scaled_r - 4, y1,
                    x2, y1 + scaled_r,
                    x2, y2 - scaled_r,
                    x2 - scaled_r - 4, y2
                ]
            elif stripe_pos == "Top":
                stripe_poly = [
                    x1 + scaled_r, y1,
                    x2 - scaled_r, y1,
                    x2, y1 + 4,
                    x1, y1 + 4
                ]
            elif stripe_pos == "Bottom":
                stripe_poly = [
                    x1 + scaled_r, y2 - 4,
                    x2 - scaled_r, y2 - 4,
                    x2, y2,
                    x1, y2
                ]
            else: # Left
                stripe_poly = [
                    x1 + scaled_r, y1,
                    x1 + scaled_r + 4, y1,
                    x1 + scaled_r + 4, y2,
                    x1 + scaled_r, y2,
                    x1, y2 - scaled_r,
                    x1, y1 + scaled_r
                ]
            canvas.create_polygon(stripe_poly, smooth=True, fill=accent_col)

        msg_font = (font_family, int(font_size * scale), font_weight)
        sub_font = (font_family, max(6, int((font_size - 2) * scale)))

        align_key = f"{prefix}text_align"
        if align_key in self.entries:
            text_align = self.entries[align_key][0].get()
        else:
            text_align = self.settings.get(align_key, "left")

        anchor = tk.W
        tx = x1 + int((padx + 10) * scale)
        if text_align == "center":
            anchor = tk.CENTER
            tx = x1 + scaled_w // 2
        elif text_align == "right":
            anchor = tk.E
            tx = x2 - int((padx + 10) * scale)

        if toast_type == "Health Tip":
            canvas.create_text(
                tx,
                y1 + scaled_h // 2,
                anchor=anchor,
                text=f"{emoji}  {message}",
                font=msg_font,
                fill=fg_col,
                width=scaled_w - int((padx + 10) * 2 * scale),
            )
        elif toast_type == "Brightness Care":
            title_font = ("Consolas", int(12 * scale), "bold")
            sub_font = ("Consolas", int(10 * scale))

            canvas.create_text(
                x1 + scaled_w // 2,
                y1 + int(25 * scale),
                anchor=tk.CENTER,
                text=title,
                font=title_font,
                fill=accent_col,
            )
            canvas.create_text(
                x1 + scaled_w // 2,
                y1 + int(55 * scale),
                anchor=tk.CENTER,
                text=message,
                font=sub_font,
                fill=fg_col,
            )

            btn_w = int(80 * scale)
            btn_h = int(22 * scale)
            btn_y1 = y1 + int(90 * scale)
            btn_y2 = btn_y1 + btn_h

            skip_x1 = x1 + scaled_w // 2 - btn_w - int(10 * scale)
            skip_x2 = skip_x1 + btn_w
            canvas.create_rectangle(
                skip_x1, btn_y1, skip_x2, btn_y2,
                fill="#1a233a", outline="", width=0
            )
            canvas.create_text(
                (skip_x1 + skip_x2) // 2, (btn_y1 + btn_y2) // 2,
                text="SKIP", font=("Consolas", int(8 * scale), "bold"), fill=fg_col
            )

            dec_x1 = x1 + scaled_w // 2 + int(10 * scale)
            dec_x2 = dec_x1 + btn_w
            canvas.create_rectangle(
                dec_x1, btn_y1, dec_x2, btn_y2,
                fill=accent_col, outline="", width=0
            )
            canvas.create_text(
                (dec_x1 + dec_x2) // 2, (btn_y1 + btn_y2) // 2,
                text="DECREASE", font=("Consolas", int(8 * scale), "bold"), fill="#070b14"
            )
        else:  # General Warning or Night Care
            canvas.create_text(
                tx,
                y1 + int(pady * scale),
                anchor=anchor,
                text=f"{emoji}  {title}",
                font=msg_font,
                fill=fg_col,
            )
            canvas.create_text(
                tx,
                y1 + int((pady + font_size + 8) * scale),
                anchor=anchor,
                text=message,
                font=sub_font,
                fill="#8892b0",
                width=scaled_w - int((padx + 10) * 2 * scale),
            )

    def _test_preview_sound_for_tab(self, tab_name):
        toast_type = self._get_toast_type_for_tab(tab_name)
        if not toast_type:
            return
        if toast_type == "General Warning":
            prefix = "toast_"
        elif toast_type == "Health Tip":
            prefix = "ht_toast_"
        elif toast_type == "Brightness Care":
            prefix = "bc_toast_"
        else:
            prefix = "nc_toast_"

        snd_key = f"{prefix}sound_effect"
        if snd_key in self.entries:
            snd_choice = self.entries[snd_key][0].get()
        else:
            snd_choice = self.settings.get(snd_key, "mac_connect")

        vol_key = f"{prefix}volume"
        if vol_key in self.entries:
            volume = float(self.entries[vol_key][0].get())
        else:
            volume = float(self.settings.get(vol_key, 80))

        try:
            import winsound

            system_aliases = [
                "SystemAsterisk",
                "SystemExclamation",
                "SystemHand",
                "SystemQuestion",
                "SystemDefault",
            ]
            
            if snd_choice in system_aliases:
                winsound.PlaySound(snd_choice, winsound.SND_ALIAS | winsound.SND_ASYNC)
                return

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

            try:
                import pygame
                if pygame.mixer.get_init() and path and os.path.exists(path):
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(volume / 100.0)
                    sound.play()
                    return
            except Exception:
                pass

            if os.path.exists(path):
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            logger.error(f"Error testing sound: {e}")

    def _show_desktop_preview_for_tab(self, tab_name):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        toast_type = self._get_toast_type_for_tab(tab_name)
        if not toast_type:
            return

        temp_settings = dict(self.settings)
        temp_settings["is_preview"] = True
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                ):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(val)
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if toast_type == "General Warning":
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False
            toast = BaseToast(
                self.parent, "EYE BREAK", "Time to take a break!", temp_settings
            )
            toast.show()
            self.live_preview_toast = toast
        elif toast_type == "Health Tip":
            temp_settings["ht_toast_auto_dismiss"] = False
            temp_settings["ht_toast_enable_sound"] = False
            toast = BaseToast(
                self.parent,
                "HEALTH TIP",
                "Take a slow, deep breath. Inhale for 4s.",
                temp_settings,
                is_health_tip=True,
            )
            toast.show()
            self.live_preview_toast = toast
        elif toast_type == "Brightness Care":
            temp_settings["bc_safe_duration_seconds"] = 999999
            temp_settings["bc_toast_enable_sound"] = False
            
            def _on_skip():
                pass
            def _on_decrease():
                pass
                
            toast = BrightnessWarningToast(
                self.parent, temp_settings, _on_skip, _on_decrease
            )
            toast.show()
            self.live_preview_toast = toast
        else:  # Night Care
            nc_settings = dict(temp_settings)
            for k, v in temp_settings.items():
                if k.startswith("nc_toast_"):
                    suffix = k[len("nc_toast_"):]
                    nc_settings[f"toast_{suffix}"] = v
            nc_settings["toast_auto_dismiss"] = False
            nc_settings["toast_enable_sound"] = False
            toast = BaseToast(
                self.parent,
                "NIGHT CARE",
                "It's late. Your body needs rest. 🌙",
                nc_settings,
            )
            toast.show()
            self.live_preview_toast = toast

    def _save_silently(self):
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                ):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        save_settings(self.settings)
        self.on_save(self.settings)

    def _restore_defaults(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to restore all settings to default? This cannot be undone."):
            self.settings = dict(DEFAULT_SETTINGS)
            for key, (var, var_type) in self.entries.items():
                val = self.settings.get(key, "")
                if var_type == "bool":
                    var.set(bool(val))
                else:
                    var.set(str(val))
            self._on_settings_modified()

    def _save_and_close(self, root):
        if hasattr(self, "live_preview_toast") and self.live_preview_toast:
            try:
                self.live_preview_toast.force_close()
            except Exception:
                pass
            self.live_preview_toast = None

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                ):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(val)
                else:
                    self.settings[key] = val
            except ValueError:
                pass

        save_settings(self.settings)
        self.on_save(self.settings)
        
        for key in list(self.entries.keys()):
            var, var_type = self.entries.pop(key)
            del var

        root.grab_release()
        root.destroy()

    def _update_upcoming_break(self):
        if not hasattr(self, "upcoming_title_label") or not self.upcoming_title_label.winfo_exists():
            return

        if not self.app:
            self.upcoming_type_label.config(text="N/A")
            self.upcoming_time_label.config(text="--:--")
            self.upcoming_clock_label.config(text="No App Connection")
            return

        now = time.time()
        
        # Calculate next break times using settings values
        short_interval = self.app.settings.get("short_break_interval_min", 20) * 60
        long_interval = self.app.settings.get("long_break_interval_min", 60) * 60
        
        next_short = self.app._last_short_break + short_interval
        next_long = self.app._last_long_break + long_interval
        
        # Determine which break is sooner
        if next_long <= next_short:
            break_type = "Long Break"
            next_break_time = next_long
        else:
            break_type = "Short Break"
            next_break_time = next_short
            
        remaining = next_break_time - now
        
        if self.app._paused:
            self.upcoming_type_label.config(text=break_type, fg=TH["warning"])
            self.upcoming_time_label.config(text="PAUSED")
            
            # Format scheduled time
            local_time_struct = time.localtime(next_break_time)
            time_str = time.strftime("%H:%M:%S", local_time_struct)
            self.upcoming_clock_label.config(text=f"Scheduled at {time_str}")
        elif remaining <= 0:
            self.upcoming_type_label.config(text=break_type, fg=TH["accent"])
            self.upcoming_time_label.config(text="00m 00s")
            self.upcoming_clock_label.config(text="Starting...")
        else:
            self.upcoming_type_label.config(text=break_type, fg=TH["accent"])
            
            # Format remaining time (e.g., "12m 45s" or "45s")
            rem_sec = int(remaining)
            rem_min = rem_sec // 60
            rem_sec = rem_sec % 60
            if rem_min > 0:
                time_text = f"{rem_min:02d}m {rem_sec:02d}s"
            else:
                time_text = f"{rem_sec:02d}s"
            self.upcoming_time_label.config(text=time_text)
            
            # Format scheduled time
            local_time_struct = time.localtime(next_break_time)
            time_str = time.strftime("%H:%M:%S", local_time_struct)
            self.upcoming_clock_label.config(text=f"at {time_str}")
            
        # Schedule next update in 1 second
        self.sidebar.after(1000, self._update_upcoming_break)
