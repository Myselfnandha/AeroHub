import tkinter as tk
from tkinter import ttk, colorchooser
import sys
import os

# AeroHub Theme
TH = {
    "bg": "#0a0a1a",
    "bg2": "#12122a",
    "bg3": "#1e1e3f",
    "accent": "#ff3366",  # Red/pink accent for temp
    "accent_hover": "#ff6688",
    "fg": "#f0f0f0",
    "fg_dim": "#a0a0b0",
    "border": "#2d2d5e",
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(SCRIPT_DIR))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from services.aerohub_core.toast_utils import BaseToast, EmojiPickerPanel
except ImportError:
    pass


class SettingsWindow:
    def __init__(self, root, current_settings, on_save_callback):
        self.parent = root
        self.settings = current_settings
        self.on_save = on_save_callback

        self.entries = {}
        self.window = tk.Toplevel(root)
        self.window.title("Temperature Monitor Settings")
        self.window.geometry("800x600")
        self.window.configure(bg=TH["bg"])

        # Scan available sounds
        sounds_dir = os.path.join(SCRIPT_DIR, "sounds")
        wav_files = []
        if os.path.exists(sounds_dir):
            try:
                wav_files = [
                    os.path.splitext(f)[0]
                    for f in os.listdir(sounds_dir)
                    if f.endswith(".wav")
                ]
            except Exception:
                pass
        system_sounds = [
            "SystemAsterisk",
            "SystemExclamation",
            "SystemHand",
            "SystemQuestion",
            "SystemDefault",
        ]
        self.sound_choices = sorted(wav_files) + system_sounds

        # Apply rounded corners
        try:
            import ctypes

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.window.wm_frame(), 16),
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(2)),
                ctypes.sizeof(ctypes.c_int),
            )
        except Exception:
            pass

        try:
            from PIL import ImageTk
            from toggles.temp_monitor.temp_monitor import create_temp_icon
            icon_img = create_temp_icon(45.0)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            self.window.iconphoto(False, self.icon_photo)
        except Exception:
            pass

        def on_closing():
            if hasattr(self, "preview_instances") and self.preview_instances:
                for t in list(self.preview_instances):
                    try:
                        t.force_close()
                    except Exception:
                        pass
                self.preview_instances = []
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self._build_ui()

    def _build_ui(self):
        main_container = tk.Frame(self.window, bg=TH["bg"])
        main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_container, bg=TH["bg2"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="TEMP.SYS",
            font=("Consolas", 18, "bold"),
            bg=TH["bg2"],
            fg=TH["accent"],
        ).pack(pady=(30, 40))

        self.content_area = tk.Frame(main_container, bg=TH["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        f_general = tk.Frame(self.content_area, bg=TH["bg"])
        f_toast = tk.Frame(self.content_area, bg=TH["bg"])

        self.frames = {"General": f_general, "Toast FX": f_toast}

        self._build_general_tab(f_general)
        self._build_toast_tab(f_toast)

        self.current_frame = None
        self.nav_buttons = {}

        def switch_tab(name):
            if self.current_frame:
                self.current_frame.pack_forget()
                self.nav_buttons[self.current_frame_name].config(
                    bg=TH["bg2"], fg=TH["fg_dim"]
                )
            self.current_frame = self.frames[name]
            self.current_frame_name = name
            self.current_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
            self.nav_buttons[name].config(bg=TH["bg3"], fg=TH["accent"])

        for name in ["General", "Toast FX"]:
            btn = tk.Button(
                self.sidebar,
                text=f"■ {name.upper()}",
                font=("Consolas", 11, "bold"),
                bg=TH["bg2"],
                fg=TH["fg_dim"],
                activebackground=TH["bg3"],
                activeforeground=TH["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda n=name: switch_tab(n),
            )
            btn.pack(fill=tk.X, pady=4)
            self.nav_buttons[name] = btn

        self.btn_save = tk.Button(
            self.sidebar,
            text="[ SAVE_CFG ]",
            font=("Consolas", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=12,
            command=self._save_settings_clicked,
        )
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=24)

        switch_tab("General")

    def _add_field(self, parent_frame, label, key, row, is_str=False):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
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
            width=14,
        ).grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, is_str)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _add_combo(self, parent_frame, label, key, row, values):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, values[0])))

        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))

        if key.endswith("_sound_effect") or "sound_" in key:
            prefix = "toast_" if key.startswith("toast_") else ""
            btn_test = tk.Button(
                f,
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
            def on_enter(e, b=btn_test): b.config(bg=TH["bg2"])
            def on_leave(e, b=btn_test): b.config(bg=TH["bg3"])
            btn_test.bind("<Enter>", on_enter)
            btn_test.bind("<Leave>", on_leave)

        combo = ttk.Combobox(
            f,
            textvariable=var,
            values=values,
            font=("Consolas", 10),
            state="readonly",
            width=12,
        )
        combo.pack(side=tk.LEFT)

        self.entries[key] = (var, True)
        if key.startswith("toast_"):
            var.trace_add("write", lambda *args: self._schedule_preview())

    def _test_sound_by_key_and_prefix(self, key, prefix):
        if key in self.entries:
            snd_choice = self.entries[key][0].get()
        else:
            snd_choice = self.settings.get(key, "mac_connect")
        if not snd_choice or snd_choice == "None":
            return

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

            # Look in temp_monitor sounds first, then health_app resources, then battery_monitor
            path = os.path.join(SCRIPT_DIR, "sounds", snd_choice)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "services", "health_app", "resources", "sounds", snd_choice)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(SCRIPT_DIR), "battery_monitor", "sounds", snd_choice)

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
            print(f"Error testing sound: {e}")

    def _add_color_field(self, parent_frame, label, key, row):
        tk.Label(
            parent_frame,
            text=label.upper(),
            font=("Consolas", 9),
            bg=TH["bg"],
            fg=TH["fg_dim"],
            anchor=tk.W,
        ).grid(row=row, column=0, sticky=tk.W, pady=8)
        var = tk.StringVar(value=str(self.settings.get(key, "")))

        def choose_color(v=var):
            c = colorchooser.askcolor(initialcolor=v.get())[1]
            if c:
                v.set(c)
                btn.config(bg=c)

        btn = tk.Button(
            parent_frame,
            bg=var.get(),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
            command=choose_color,
        )
        btn.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        self.entries[key] = (var, True)
        if key.startswith("toast_"):
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
        if key.startswith("toast_"):
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
        var = tk.StringVar(value=str(self.settings.get(key, "🔥")))
        f = tk.Frame(parent_frame, bg=TH["bg"])
        f.grid(row=row, column=1, sticky=tk.E, pady=8, padx=(20, 0))
        lbl = tk.Label(
            f, textvariable=var, font=("Segoe UI Emoji", 12), bg=TH["bg"], fg=TH["fg"]
        )
        lbl.pack(side=tk.LEFT, padx=(0, 5))

        def _on_select(emoji):
            var.set(emoji)
            if key.startswith("toast_"):
                self._schedule_preview()

        def _open_picker():
            EmojiPickerPanel(self.window, _on_select)

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

    def _build_general_tab(self, tab):
        tk.Label(
            tab,
            text="THERMAL THRESHOLDS",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 20))
        f1 = tk.Frame(tab, bg=TH["bg"])
        f1.pack(fill=tk.X)
        self._add_field(f1, "Warning Temp (°C):", "warning_temp", 0)
        self._add_field(f1, "Critical Temp (°C):", "critical_temp", 1)

    def _build_toast_tab(self, tab):
        tk.Label(
            tab,
            text="UI / UX CONFIG",
            font=("Consolas", 14, "bold"),
            bg=TH["bg"],
            fg=TH["fg"],
        ).pack(anchor=tk.W, pady=(0, 10))
        canvas = tk.Canvas(tab, bg=TH["bg"], highlightthickness=0)
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

        tab.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        f_top = tk.Frame(scrollable_frame, bg=TH["bg"])
        f_top.pack(fill=tk.BOTH, expand=True)
        f2_left = tk.Frame(f_top, bg=TH["bg"])
        f2_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
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
        self._add_field(f2_left, "Custom X (if custom):", "toast_custom_x", 4)
        self._add_field(f2_left, "Custom Y (if custom):", "toast_custom_y", 5)
        self._add_color_field(f2_left, "Background Color:", "toast_bg_color", 6)
        self._add_color_field(f2_left, "Text Color:", "toast_fg_color", 7)
        self._add_color_field(f2_left, "Accent Color:", "toast_accent_color", 8)
        self._add_combo(f2_left, "Font Family:", "toast_font_family", 9, fonts)
        self._add_field(f2_left, "Font Size:", "toast_font_size", 10)
        self._add_combo(
            f2_left, "Font Weight:", "toast_font_weight", 11, ["normal", "bold"]
        )
        self._add_combo(
            f2_left, "Text Align:", "toast_text_align", 12, ["left", "center", "right"]
        )

        self._add_emoji_picker(f2_right, "Emoji Icon:", "toast_emoji", 0)
        self._add_field(f2_right, "Border Radius (px):", "toast_radius", 1)
        self._add_field(f2_right, "Padding X (px):", "toast_padding_x", 2)
        self._add_field(f2_right, "Padding Y (px):", "toast_padding_y", 3)
        self._add_field(f2_right, "Opacity (0.1 - 1.0):", "toast_opacity", 4)
        self._add_field(f2_right, "Border Width (px):", "toast_border_width", 5)
        self._add_color_field(f2_right, "Border Color:", "toast_border_color", 6)
        self._add_color_field(f2_right, "Gradient End Color:", "toast_gradient_end", 7)
        self._add_combo(f2_right, "Click Action:", "toast_click_action", 8, actions)
        self._add_field(f2_right, "Duration (sec):", "toast_duration_sec", 9)
        self._add_field(f2_right, "Transition (ms):", "toast_transition_time_ms", 10)
        self._add_combo(f2_right, "Sound Effect:", "toast_sound_effect", 11, self.sound_choices)

        f3 = tk.Frame(scrollable_frame, bg=TH["bg"])
        f3.pack(fill=tk.X, pady=(15, 0))

        self._add_grid_chk(f3, "Enable Shadow/Glow", "toast_shadow", 0)
        self._add_grid_chk(f3, "Enable Gradient BG", "toast_gradient", 1)
        self._add_grid_chk(f3, "Enable Accent Stripe", "toast_accent_stripe", 2)
        self._add_grid_chk(f3, "Show Progress Bar", "toast_progress_bar", 3)
        self._add_grid_chk(f3, "Auto-Dismiss", "toast_auto_dismiss", 4)
        self._add_grid_chk(f3, "Play Warning Sound", "toast_enable_sound", 5)

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

    def _schedule_preview(self):
        self._preview_toast(is_auto_edit=True)

    def _preview_toast(self, is_auto_edit=False):
        if hasattr(self, "preview_instances") and self.preview_instances:
            for t in list(self.preview_instances):
                try:
                    t.force_close()
                except Exception:
                    pass
            self.preview_instances = []
        else:
            self.preview_instances = []

        temp_settings = dict(self.settings)
        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    temp_settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    temp_settings[key] = float(val)
                elif var_type is False:
                    temp_settings[key] = int(float(val))
                else:
                    temp_settings[key] = val
            except ValueError:
                pass

        if is_auto_edit:
            temp_settings["toast_auto_dismiss"] = False
            temp_settings["toast_enable_sound"] = False

        temp_settings["is_preview"] = True

        previews = [
            ("TEMPERATURE WARNING", f"CPU temperature has exceeded {temp_settings.get('warning_temp', 65)}°C. 🔥"),
            ("CRITICAL TEMPERATURE", f"CPU temperature has exceeded {temp_settings.get('critical_temp', 70)}°C! Shutting down... ⚠️")
        ]

        for title, msg in previews:
            t = BaseToast(self.window, title, msg, temp_settings)
            t.show()
            self.preview_instances.append(t)

    def _save_settings_clicked(self):
        if hasattr(self, "preview_instances") and self.preview_instances:
            for t in list(self.preview_instances):
                try:
                    t.force_close()
                except Exception:
                    pass
            self.preview_instances = []

        for key, (var, var_type) in self.entries.items():
            val = var.get()
            try:
                if var_type == "bool":
                    self.settings[key] = val == "1" or val == "True" or val is True
                elif key in ("toast_opacity",):
                    self.settings[key] = float(val)
                elif var_type is False:
                    self.settings[key] = int(float(val))
                else:
                    self.settings[key] = val
            except ValueError:
                pass
        self.on_save(self.settings)

        self.btn_save.config(text="[ SAVED ]", state=tk.DISABLED)
        def reset_btn():
            try:
                self.btn_save.config(text="[ SAVE_CFG ]", state=tk.NORMAL)
            except Exception:
                pass
        self.window.after(2000, reset_btn)
