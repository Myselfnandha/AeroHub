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
from ui.toast import BrightnessWarningToast, WarningToast
from services.aerohub_core.toast_utils import BaseToast
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
        self.live_preview_toasts = []
        self.live_preview_tab = None

        # Pre-populate location check interval display value
        interval_map = {0: "Disabled", 1: "Every Hour", 2: "Every 2 Hours", 6: "Every 6 Hours", 12: "Every 12 Hours", 24: "Every 24 Hours"}
        val = self.settings.get("location_check_interval_hours", 1)
        self.settings["location_check_interval_display"] = interval_map.get(val, "Every Hour")

    def show(self):
        self._create()

    def _create(self):
        root = tk.Toplevel(self.parent)
        root.transient(None)
        root.title("SYSTEM OVERRIDE // HEALTH CONFIG")
        root.configure(bg=TH["bg"])
        root.resizable(True, True)

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
            try:
                self._save_silently()
            except Exception as e:
                logger.error(f"Error auto-saving settings on close: {e}")
                    
            if hasattr(self, "live_preview_toasts") and self.live_preview_toasts:
                for t in list(self.live_preview_toasts):
                    try:
                        t.force_close()
                    except Exception:
                        pass
                self.live_preview_toasts = []
                
            for key in list(self.entries.keys()):
                try:
                    if key in self.entries:
                        var, var_type = self.entries.pop(key)
                        del var
                except Exception:
                    pass

            if self.app:
                try:
                    self.app._settings_window = None
                except Exception:
                    pass

            try:
                root.destroy()
            except Exception as e:
                logger.error(f"Error destroying root settings window: {e}")

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Centered settings window / maximized on start
        root.update_idletasks()
        w = 650
        h = 700
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(580, 600)
        try:
            root.state("zoomed")
        except Exception:
            pass

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
        ).pack(pady=(32, 0))

        btn_restore = tk.Button(
            self.sidebar,
            text="Reset Defaults",
            font=("Segoe UI", 8, "underline"),
            bg=TH["bg2"],
            fg=TH["fg_dim"],
            activebackground=TH["bg2"],
            activeforeground=TH["danger"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._restore_defaults,
        )
        btn_restore.pack(pady=(0, 20))
        _add_hover(btn_restore, TH["bg2"], TH["bg2"], TH["fg_dim"], TH["danger"])
        
        # Zeigarnik Effect: Active Modules Dashboard
        self.status_frame = tk.Frame(self.sidebar, bg=TH["bg3"], padx=10, pady=10)
        self.status_frame.pack(fill=tk.X, padx=15, pady=(0, 20))
        
        tk.Label(self.status_frame, text="SYSTEM STATUS", font=("Consolas", 8, "bold"), bg=TH["bg3"], fg=TH["fg_dim"]).pack(anchor=tk.W)
        self.lbl_status_nl = tk.Label(self.status_frame, text="○ Night Light", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_nl.pack(anchor=tk.W, pady=(4, 0))
        self.lbl_status_ht = tk.Label(self.status_frame, text="○ Health Tips", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_ht.pack(anchor=tk.W)
        self.lbl_status_bc = tk.Label(self.status_frame, text="○ Brightness Care", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_bc.pack(anchor=tk.W)
        self.lbl_status_nc = tk.Label(self.status_frame, text="○ Night Care", font=("Consolas", 9), bg=TH["bg3"], fg=TH["fg_dim"])
        self.lbl_status_nc.pack(anchor=tk.W)

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

        for name in self.nav_names:
            tab_container = tk.Frame(self.content_area, bg=TH["bg"])
            self.frames[name] = tab_container

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
            if hasattr(self, "live_preview_toasts") and self.live_preview_toasts:
                self._save_silently()
                for t in list(self.live_preview_toasts):
                    try:
                        t.force_close()
                    except Exception:
                        pass
                self.live_preview_toasts = []

            if self.current_frame:
                self.current_frame.pack_forget()
                self._style_tab_button(self.current_frame_name, active=False)

            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            self._style_tab_button(name, active=True)
            self._on_settings_modified(is_tab_switch=True)

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
        self.btn_save = tk.Button(
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
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(5, 20))
        _add_hover(self.btn_save, TH["accent"], TH["accent_hover"], "#000000", "#000000")

        self.lbl_saved = tk.Label(
            self.sidebar, text="", font=("Segoe UI", 10, "bold"), bg=TH["bg2"], fg=TH["success"]
        )
        self.lbl_saved.pack(side=tk.BOTTOM, pady=(10, 0))



        # Play Preview Button in Sidebar
        self.btn_preview = tk.Button(
            self.sidebar,
            text="▶ Play Preview",
            font=("Segoe UI", 11, "bold"),
            bg=TH["bg3"],
            fg=TH["fg"],
            activebackground=TH["accent"],
            activeforeground="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            pady=16,
            command=self._play_preview_clicked,
        )
        self.btn_preview.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=(5, 5))
        _add_hover(self.btn_preview, TH["bg3"], TH["accent"], TH["fg"], "#000000")

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
            font=("Segoe UI", 14, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
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
            insertbackground=TH["fg"],
            relief=tk.FLAT,
        )
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.entries[key] = (var, is_str)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return entry

    def _add_slider_field(self, parent_frame, label, key, row, col=0, from_=0, to=100, resolution=1):
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

        val = self.settings.get(key, from_)
        try:
            val = float(val)
        except (ValueError, TypeError):
            val = float(from_)
        var = tk.DoubleVar(value=val)
        slider = tk.Scale(
            cell,
            variable=var,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            bg=bg,
            fg=TH["fg"],
            troughcolor=TH["bg"],
            highlightthickness=0,
            activebackground=TH["accent"],
            length=120,
            showvalue=True
        )
        slider.pack(side=tk.RIGHT)

        # Store as string variable to match standard format
        str_var = tk.StringVar(value=str(var.get()))
        def _update_str(*args):
            str_var.set(str(var.get()))
        var.trace_add("write", _update_str)

        self.entries[key] = (str_var, False)
        str_var.trace_add("write", lambda *args: self._on_settings_modified())
        return slider

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

        if key.endswith("_sound_effect"):
            prefix = key[:-len("sound_effect")]
            btn_test = tk.Button(
                cell,
                text="🔊",
                font=("Segoe UI Symbol", 8),
                bg=TH["bg3"],
                fg=TH["accent"],
                activebackground=TH["bg2"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                width=3,
                command=lambda k=key, p=prefix: self._test_sound_by_key_and_prefix(k, p)
            )
            btn_test.pack(side=tk.RIGHT, padx=(5, 0))
            _add_hover(btn_test, TH["bg3"], TH["bg2"], TH["accent"], TH["accent"])

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

    def _test_sound_by_key_and_prefix(self, key, prefix):
        if key in self.entries:
            snd_choice = self.entries[key][0].get()
        else:
            snd_choice = self.settings.get(key, "mac_connect")

        vol_key = f"{prefix}volume"
        if vol_key in self.entries:
            try:
                volume = float(self.entries[vol_key][0].get())
            except ValueError:
                volume = 80.0
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
                self._on_settings_modified()

        btn = tk.Button(
            cell,
            bg=var.get() if var.get() else TH["accent"],
            width=3,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.pack(side=tk.RIGHT, padx=(10, 0))

        entry = tk.Entry(
            cell,
            textvariable=var,
            width=9,
            font=("Consolas", 10),
            bg=TH["bg3"],
            fg=TH["fg"],
            insertbackground=TH["fg"],
            relief=tk.FLAT,
        )
        entry.pack(side=tk.RIGHT)

        def _update_btn_bg(*args):
            try:
                # Basic validation for hex
                val = var.get().strip()
                if val.startswith("#") and len(val) in (4, 7):
                    btn.config(bg=val)
            except Exception:
                pass

        var.trace_add("write", _update_btn_bg)
        self.entries[key] = (var, True)
        var.trace_add("write", lambda *args: self._on_settings_modified())
        return entry

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
        
        def _auto_detect():
            import urllib.request
            import json
            try:
                btn_detect.config(text="Detecting...")
                btn_detect.update()
                with urllib.request.urlopen("http://ip-api.com/json/", timeout=5) as r:
                    data = json.loads(r.read().decode())
                    if "lat" in data and "lon" in data:
                        self.entries["latitude"][0].set(str(data["lat"]))
                        self.entries["longitude"][0].set(str(data["lon"]))
            except Exception:
                pass
            finally:
                btn_detect.config(text="Auto-Detect IP")

        btn_detect = tk.Button(f2, text="Auto-Detect IP", font=("Consolas", 8), bg=TH["bg3"], fg=TH["fg"], relief=tk.FLAT, cursor="hand2", command=_auto_detect)
        btn_detect.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        self._add_field(f2, "Night Start (hr):", "night_light_start_hour", 2, col=0)
        self._add_field(f2, "Night End (hr):", "night_light_end_hour", 2, col=1)
        self._add_field(f2, "Transition (sec):", "nl_transition_duration", 3, col=0)
        
        location_options = [
            "Disabled", "Every Hour", "Every 2 Hours", "Every 6 Hours", "Every 12 Hours", "Every 24 Hours"
        ]
        self._add_combo(f2, "Location Auto-Check:", "location_check_interval_display", 3, location_options, col=1)

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
        
        self._add_slider_field(f4, "Volume (0-100):", "voice_volume", 3, col=0, from_=0, to=100, resolution=1)
        self._add_slider_field(f4, "Speed Rate:", "voice_rate", 3, col=1, from_=-10, to=10, resolution=1)
        
        self._add_combo(f4, "Break Type:", "voice_break_type", 4, ["Both", "Short Only", "Long Only"], col=0)
        self._add_field(f4, "Min Duration (s):", "voice_min_duration_sec", 4, col=1)

        self._add_slider_field(f4, "Voice Pitch:", "voice_pitch", 5, col=0, from_=-10, to=10, resolution=1)
        self._add_slider_field(f4, "Start Delay (s):", "voice_start_delay_sec", 5, col=1, from_=0, to=10, resolution=1)
        
        self._add_field(f4, "Inhale Text:", "voice_inhale_text", 6, col=0, is_str=True)
        self._add_field(f4, "Exhale Text:", "voice_exhale_text", 6, col=1, is_str=True)
        self._add_field(f4, "Hold In Text:", "voice_hold_in_text", 7, col=0, is_str=True)
        self._add_field(f4, "Hold Out Text:", "voice_hold_out_text", 7, col=1, is_str=True)

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
        self._add_grid_chk(f1, "Show Clock Time", "toast_show_clock", 5, col=0)

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
        self._add_slider_field(f2, "Opacity:", "toast_opacity", 4, col=1, from_=0.1, to=1.0, resolution=0.05)
        self._add_grid_chk(f2, "Enable Gradient", "toast_gradient", 5, col=0)
        self._add_grid_chk(f2, "Enable Shadow", "toast_shadow", 5, col=1)
        self._add_grid_chk(f2, "Accent Stripe", "toast_accent_stripe", 6, col=0)
        self._add_grid_chk(f2, "Progress Bar", "toast_progress_bar", 6, col=1)
        self._add_field(f2, "Padding X (px):", "toast_padding_x", 7, col=0)
        self._add_field(f2, "Padding Y (px):", "toast_padding_y", 7, col=1)

        card3, f3 = self._create_card(tab, "Audio & Interaction", 2, 0, columnspan=2)
        self._add_grid_chk(f3, "Play Warning Sound", "toast_enable_sound", 0, col=0)
        self._add_combo(f3, "Sound Effect:", "toast_sound_effect", 0, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "toast_volume", 1, col=0, from_=0, to=100, resolution=1)
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
        self._add_grid_chk(f1, "Show Clock Time", "ht_toast_show_clock", 3, col=0)

        card1_night, f1_night = self._create_card(tab, "Night Mode Overrides (During Night Care Hours)", 1, 0, columnspan=2)
        self._add_grid_chk(f1_night, "Enable at Night", "ht_night_enabled", 0, col=0)
        self._add_field(f1_night, "Night Interval (min):", "ht_night_interval_min", 0, col=1)
        self._add_field(f1_night, "Night Duration (sec):", "ht_night_duration_sec", 1, col=0)
        self._add_combo(
            f1_night, "Night Position:", "ht_night_toast_pos", 1, col=1,
            values=["Left", "Center", "Right", "Top-Left", "Top-Center", "Top-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Middle-Left", "Middle-Right", "Random"]
        )

        card2, f2 = self._create_card(tab, "Tip Categories", 2, 0, columnspan=2)
        self._add_grid_chk(f2, "Breathing Exercises", "ht_cat_breathing", 0, col=0)
        self._add_grid_chk(f2, "Eye Care Tips", "ht_cat_eye_care", 0, col=1)
        self._add_grid_chk(f2, "Posture Adjustment", "ht_cat_posture", 1, col=0)
        self._add_grid_chk(f2, "Muscle Stretching", "ht_cat_stretch", 1, col=1)
        self._add_grid_chk(f2, "Hydration Reminders", "ht_cat_hydration", 2, col=0)
        self._add_grid_chk(f2, "Mental Ease Moments", "ht_cat_mental", 2, col=1)
        self._add_grid_chk(f2, "Hands & Wrists", "ht_cat_hands_wrists", 3, col=0)

        card3, f3 = self._create_card(tab, "Toast Style & Audio", 3, 0, columnspan=2)
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
        self._add_slider_field(f3, "Opacity:", "ht_toast_opacity", 6, col=0, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f3, "Text Align:", "ht_toast_text_align", 6, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "ht_toast_gradient", 7, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "ht_toast_shadow", 7, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "ht_toast_accent_stripe", 8, col=0)
        self._add_grid_chk(f3, "Progress Bar", "ht_toast_progress_bar", 8, col=1)
        self._add_grid_chk(f3, "Play Tip Sound", "ht_toast_enable_sound", 9, col=0)
        self._add_combo(f3, "Sound Effect:", "ht_toast_sound_effect", 9, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "ht_toast_volume", 10, col=0, from_=0, to=100, resolution=1)
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
        self._add_slider_field(f3, "Opacity:", "bc_toast_opacity", 8, col=0, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f3, "Text Align:", "bc_toast_text_align", 8, ["left", "center", "right"], col=1)
        self._add_grid_chk(f3, "Enable Gradient", "bc_toast_gradient", 9, col=0)
        self._add_grid_chk(f3, "Enable Shadow", "bc_toast_shadow", 9, col=1)
        self._add_grid_chk(f3, "Accent Stripe", "bc_toast_accent_stripe", 10, col=0)
        self._add_grid_chk(f3, "Progress Bar", "bc_toast_progress_bar", 10, col=1)
        self._add_grid_chk(f3, "Play Warning Sound", "bc_toast_enable_sound", 11, col=0)
        self._add_combo(f3, "Sound Effect:", "bc_toast_sound_effect", 11, SOUND_EFFECTS, col=1)
        self._add_slider_field(f3, "Volume:", "bc_toast_volume", 12, col=0, from_=0, to=100, resolution=1)
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
        self._add_grid_chk(f1, "Enable Screen Flick", "nc_flick_enabled", 3, col=0)
        self._add_field(f1, "Flick Hold (sec):", "nc_flick_hold_sec", 3, col=1)
        self._add_field(f1, "Flick Fade (sec):", "nc_flick_fade_sec", 4, col=0)

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
        self._add_slider_field(f2, "Opacity:", "nc_toast_opacity", 8, col=1, from_=0.1, to=1.0, resolution=0.05)
        self._add_combo(f2, "Text Align:", "nc_toast_text_align", 9, ["left", "center", "right"], col=0)
        self._add_grid_chk(f2, "Enable Gradient", "nc_toast_gradient", 9, col=1)
        self._add_grid_chk(f2, "Enable Shadow", "nc_toast_shadow", 10, col=0)
        self._add_grid_chk(f2, "Accent Stripe", "nc_toast_accent_stripe", 10, col=1)
        self._add_grid_chk(f2, "Progress Bar", "nc_toast_progress_bar", 11, col=0)
        self._add_grid_chk(f2, "Play Warning Sound", "nc_toast_enable_sound", 11, col=1)
        self._add_combo(f2, "Sound Effect:", "nc_toast_sound_effect", 12, SOUND_EFFECTS, col=0)
        self._add_slider_field(f2, "Volume:", "nc_toast_volume", 12, col=1, from_=0, to=100, resolution=1)
        self._add_combo(f2, "Click Action:", "nc_toast_click_action", 13, ["dismiss", "snooze", "settings"], col=0)
        self._add_field(f2, "Padding X (px):", "nc_toast_padding_x", 13, col=1)
        self._add_field(f2, "Padding Y (px):", "nc_toast_padding_y", 14, col=0)

    def _get_toast_type_for_tab(self, tab_name):
        if "Toast FX" in tab_name:
            return "General Warning"
        if "Health Toast" in tab_name:
            return "Health Tip"
        if "Brightness Care" in tab_name:
            return "Brightness Care"
        if "Night Care" in tab_name:
            return "Night Care"
        return None

    def _update_status_dashboard(self):
        def _update_lbl(lbl, key):
            val = self.settings.get(key, False)
            if key in self.entries:
                val = self.entries[key][0].get()
                if isinstance(val, str):
                    val = val.lower() in ("1", "true")
            if val:
                lbl.config(text="● " + lbl.cget("text")[2:], fg=TH["success"])
            else:
                lbl.config(text="○ " + lbl.cget("text")[2:], fg=TH["fg_dim"])
        
        if hasattr(self, "lbl_status_nl"):
            _update_lbl(self.lbl_status_nl, "nl_enabled")
            _update_lbl(self.lbl_status_ht, "ht_enabled")
            _update_lbl(self.lbl_status_bc, "bc_enabled")
            _update_lbl(self.lbl_status_nc, "nc_enabled")

    def _on_settings_modified(self, is_tab_switch=False):
        self.is_dirty = True
        self._update_status_dashboard()
        if not hasattr(self, "_save_timer"):
            self._save_timer = None

        toast_type = self._get_toast_type_for_tab(self.current_frame_name)
        if toast_type:
            temp_settings = dict(self.settings)
            for key, (var, var_type) in self.entries.items():
                if var_type == "bool":
                    val = var.get()
                else:
                    val = var.get()
                    if hasattr(val, "strip"):
                        val = val.strip()
                    else:
                        val = str(val).strip()

                try:
                    if var_type == "bool":
                        temp_settings[key] = val == "1" or val == "True" or val is True
                    elif key in (
                        "latitude",
                        "longitude",
                        "toast_opacity",
                        "ht_toast_opacity",
                        "nc_toast_opacity",
                        "nc_flick_hold_sec",
                        "nc_flick_fade_sec",
                    ):
                        temp_settings[key] = float(val)
                    elif var_type is False:
                        temp_settings[key] = int(float(val))
                    else:
                        temp_settings[key] = val
                except ValueError:
                    pass

            if "Toast FX" in self.current_frame_name:
                temp_settings["toast_auto_dismiss"] = False
                temp_settings["toast_enable_sound"] = False
                temp_settings["ht_toast_auto_dismiss"] = False
                temp_settings["ht_toast_enable_sound"] = False
                temp_settings["bc_safe_duration_seconds"] = 999999
                temp_settings["bc_toast_enable_sound"] = False
                temp_settings["nc_toast_auto_dismiss"] = False
                temp_settings["nc_toast_enable_sound"] = False
            elif toast_type == "Night Care":
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

            # Check if matching toasts are already showing
            toast_exists = False
            try:
                from services.aerohub_core.toast_utils import BaseToast
                active_names = [t.__class__.__name__ for t in BaseToast._active_toasts]
                if "Toast FX" in self.current_frame_name:
                    has_warning = "WarningToast" in active_names
                    has_brightness = "BrightnessWarningToast" in active_names
                    has_tip = any(t.__class__.__name__ == "BaseToast" and getattr(t, "is_health_tip", False) for t in BaseToast._active_toasts)
                    has_night = any(t.__class__.__name__ == "BaseToast" and not getattr(t, "is_health_tip", False) and getattr(t, "title", "") == "NIGHT CARE" for t in BaseToast._active_toasts)
                    if has_warning and has_brightness and has_tip and has_night:
                        toast_exists = True
                else:
                    for t in list(BaseToast._active_toasts):
                        if toast_type == "General Warning" and t.__class__.__name__ == "WarningToast":
                            toast_exists = True
                        elif toast_type == "Brightness Care" and t.__class__.__name__ == "BrightnessWarningToast":
                            toast_exists = True
                        elif toast_type == "Health Tip" and t.__class__.__name__ == "BaseToast" and getattr(t, "is_health_tip", False):
                            toast_exists = True
                        elif toast_type == "Night Care" and t.__class__.__name__ == "BaseToast" and not getattr(t, "is_health_tip", False) and getattr(t, "title", "") == "NIGHT CARE":
                            toast_exists = True
            except Exception as e:
                logger.error(f"Error checking active toasts: {e}")

            # Update active matching toasts
            try:
                from services.aerohub_core.toast_utils import BaseToast
                for t in list(BaseToast._active_toasts):
                    is_match = False
                    if "Toast FX" in self.current_frame_name:
                        is_match = True
                    else:
                        if toast_type == "General Warning" and t.__class__.__name__ == "WarningToast":
                            is_match = True
                        elif toast_type == "Brightness Care" and t.__class__.__name__ == "BrightnessWarningToast":
                            is_match = True
                        elif toast_type == "Health Tip" and t.__class__.__name__ == "BaseToast" and getattr(t, "is_health_tip", False):
                            is_match = True
                        elif toast_type == "Night Care" and t.__class__.__name__ == "BaseToast" and not getattr(t, "is_health_tip", False) and getattr(t, "title", "") == "NIGHT CARE":
                            is_match = True
                    
                    if is_match:
                        try:
                            t.update_settings(temp_settings)
                            if not hasattr(self, "live_preview_toasts"):
                                self.live_preview_toasts = []
                            if t not in self.live_preview_toasts:
                                self.live_preview_toasts.append(t)
                        except Exception as ex:
                            logger.error(f"Error updating active toast instance: {ex}")
            except Exception as e:
                logger.error(f"Error updating active toasts: {e}")

            # If no matching toast was showing and we are not switching tabs, spawn them
            if not toast_exists and not is_tab_switch:
                self._show_desktop_preview_for_tab(self.current_frame_name, is_auto_edit=True)

    def _play_preview_clicked(self):
        if self.current_frame_name:
            # First quietly save settings so the preview uses latest input values that haven't been debounced yet
            self._save_silently()
            self._show_desktop_preview_for_tab(self.current_frame_name)

    def _show_desktop_preview_for_tab(self, tab_name, is_auto_edit=False):
        if hasattr(self, "live_preview_toasts") and self.live_preview_toasts:
            for t in list(self.live_preview_toasts):
                try:
                    t.force_close()
                except Exception:
                    pass
            self.live_preview_toasts = []
        else:
            self.live_preview_toasts = []

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
                    temp_settings[key] = int(float(val))
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit or "Toast FX" in tab_name:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False
            temp_settings["ht_toast_auto_dismiss"] = False
            temp_settings["ht_toast_enable_sound"] = False
            temp_settings["bc_safe_duration_seconds"] = 999999
            temp_settings["bc_toast_enable_sound"] = False
            temp_settings["nc_toast_auto_dismiss"] = False
            temp_settings["nc_toast_enable_sound"] = False

        if "Toast FX" in tab_name:
            # Spawn all 4 stacked preview toasts
            # 1. General Warning
            t_warn = WarningToast(
                self.parent, "Time to take a break!", 30, temp_settings
            )
            t_warn.show()
            self.live_preview_toasts.append(t_warn)

            # 2. Health Tip
            t_tip = BaseToast(
                self.parent,
                "HEALTH TIP",
                "Take a slow, deep breath. Inhale for 4s.",
                temp_settings,
                is_health_tip=True,
            )
            t_tip.show()
            self.live_preview_toasts.append(t_tip)

            # 3. Brightness Care
            def _on_skip():
                pass
            def _on_decrease():
                pass
            t_bright = BrightnessWarningToast(
                self.parent, temp_settings, _on_skip, _on_decrease
            )
            t_bright.show()
            self.live_preview_toasts.append(t_bright)

            # 4. Night Care
            nc_settings = dict(temp_settings)
            for k, v in temp_settings.items():
                if k.startswith("nc_toast_"):
                    suffix = k[len("nc_toast_"):]
                    nc_settings[f"toast_{suffix}"] = v
            t_night = BaseToast(
                self.parent,
                "NIGHT CARE",
                "It's late. Your body needs rest. 🌙",
                nc_settings,
            )
            t_night.show()
            self.live_preview_toasts.append(t_night)
        else:
            if toast_type == "General Warning":
                toast = WarningToast(
                    self.parent, "Time to take a break!", 30, temp_settings
                )
                toast.show()
                self.live_preview_toasts.append(toast)
            elif toast_type == "Health Tip":
                toast = BaseToast(
                    self.parent,
                    "HEALTH TIP",
                    "Take a slow, deep breath. Inhale for 4s.",
                    temp_settings,
                    is_health_tip=True,
                )
                toast.show()
                self.live_preview_toasts.append(toast)
            elif toast_type == "Brightness Care":
                def _on_skip():
                    pass
                def _on_decrease():
                    pass
                toast = BrightnessWarningToast(
                    self.parent, temp_settings, _on_skip, _on_decrease
                )
                toast.show()
                self.live_preview_toasts.append(toast)
            else:  # Night Care
                nc_settings = dict(temp_settings)
                for k, v in temp_settings.items():
                    if k.startswith("nc_toast_"):
                        suffix = k[len("nc_toast_"):]
                        nc_settings[f"toast_{suffix}"] = v
                toast = BaseToast(
                    self.parent,
                    "NIGHT CARE",
                    "It's late. Your body needs rest. 🌙",
                    nc_settings,
                )
                toast.show()
                self.live_preview_toasts.append(toast)

    def _save_silently(self):
        from core.constants import DEFAULT_SETTINGS
        for key, (var, var_type) in self.entries.items():
            if var_type == "bool":
                val = var.get()
            else:
                val = var.get().strip()
            
            # Apply default if blank
            if val == "" and var_type != "bool":
                default_val = DEFAULT_SETTINGS.get(key, "")
                var.set(str(default_val))
                val = str(default_val)

            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in (
                    "latitude",
                    "longitude",
                    "toast_opacity",
                    "ht_toast_opacity",
                    "nc_toast_opacity",
                    "nc_flick_hold_sec",
                    "nc_flick_fade_sec",
                ):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(float(val))
                else:
                    self.settings[key] = val
            except ValueError:
                # Revert to last valid setting
                last_valid = self.settings.get(key, DEFAULT_SETTINGS.get(key, ""))
                var.set(str(last_valid))

        # Map display interval back to integer hours
        interval_map = {"Disabled": 0, "Every Hour": 1, "Every 2 Hours": 2, "Every 6 Hours": 6, "Every 12 Hours": 12, "Every 24 Hours": 24}
        display_val = self.settings.get("location_check_interval_display", "Every Hour")
        self.settings["location_check_interval_hours"] = interval_map.get(display_val, 1)
        if "location_check_interval_display" in self.settings:
            del self.settings["location_check_interval_display"]

        save_settings(self.settings)
        self.on_save(self.settings)
        self.is_dirty = False
        return True

    def _restore_defaults(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to restore all settings to default? This cannot be undone."):
            self.settings = dict(DEFAULT_SETTINGS)
            
            # Map location check display value
            interval_map = {0: "Disabled", 1: "Every Hour", 2: "Every 2 Hours", 6: "Every 6 Hours", 12: "Every 12 Hours", 24: "Every 24 Hours"}
            val = DEFAULT_SETTINGS.get("location_check_interval_hours", 1)
            self.settings["location_check_interval_display"] = interval_map.get(val, "Every Hour")

            for key, (var, var_type) in self.entries.items():
                val = self.settings.get(key, "")
                if var_type == "bool":
                    var.set(bool(val))
                else:
                    var.set(str(val))
            self._on_settings_modified()

    def _save_settings_clicked(self):
        if hasattr(self, "live_preview_toasts") and self.live_preview_toasts:
            for t in list(self.live_preview_toasts):
                try:
                    t.force_close()
                except Exception:
                    pass
            self.live_preview_toasts = []

        if not self._save_silently():
            return
        
        self.btn_save.config(text="Saved!", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="Save Settings", state=tk.NORMAL)
            except Exception:
                pass
        self.parent.after(2000, reset_btn)

    def _save_and_close(self, root):
        if hasattr(self, "live_preview_toasts") and self.live_preview_toasts:
            for t in list(self.live_preview_toasts):
                try:
                    t.force_close()
                except Exception:
                    pass
            self.live_preview_toasts = []

        self._save_silently()
        
        for key in list(self.entries.keys()):
            var, var_type = self.entries.pop(key)
            del var

        root.grab_release()
        root.destroy()

    def _update_upcoming_break(self):
        try:
            if not hasattr(self, "upcoming_title_label") or not self.upcoming_title_label.winfo_exists():
                return
        except Exception:
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
