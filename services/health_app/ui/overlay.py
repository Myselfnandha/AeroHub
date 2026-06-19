import os
import tkinter as tk
from core.logger import logger
from core.constants import TH
from core.media import get_media_controller
from core.audio import select_break_audio, pygame, PYGAME_AVAILABLE
from ui.theme import _add_hover

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

# Resolve path relative to HealthApp folder
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BreakOverlay:
    """Full-screen black overlay on all monitors with countdown and breathing text."""

    def __init__(
        self, parent, duration_sec: int, break_type: str, settings: dict, on_complete
    ):
        self.parent = parent
        self.duration = duration_sec
        self.break_type = break_type
        self.settings = settings
        self._remaining = duration_sec
        self._original_brightness = None
        self.status = "completed"
        self.on_complete = on_complete
        self._focus_fail_count = 0
        self._using_windowed_fallback = False

        self._voice_enabled = self.settings.get("voice_prompts_enabled", False)
        self._inhale_sec = int(self.settings.get("voice_inhale_sec", 4))
        self._hold_in_sec = int(self.settings.get("voice_hold_in_sec", 4))
        self._exhale_sec = int(self.settings.get("voice_exhale_sec", 4))
        self._hold_out_sec = int(self.settings.get("voice_hold_out_sec", 4))

    def show(self):
        """Show the overlay (non-blocking call)."""
        try:
            self._dim_screen()
            self._pause_media()
            self._create_overlay_window()
            self._play_pre_break_chime()
            self._start_countdown()
            self._start_focus_keeper()
        except Exception as e:
            logger.error(f"Break overlay error: {e}")
            self._restore()
            if self.on_complete:
                self.on_complete(self.status)

    def _dim_screen(self):
        if SBC_AVAILABLE and self.settings.get("enable_dimming"):
            try:
                self._original_brightness = sbc.get_brightness()
                logger.info("Physical brightness dimming bypassed.")
            except Exception as e:
                logger.error(f"Brightness query error: {e}")

    def _pause_media(self):
        get_media_controller().pause_active_media()
        logger.info("Executed pause for active media sessions.")

    def _play_break_audio(self):
        if not PYGAME_AVAILABLE or not self.settings.get("enable_sound"):
            return
        try:
            sound_file = select_break_audio(self.settings)
            logger.info(f"Loading break sound: {sound_file}")
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            logger.error(f"Audio play error: {e}")

    def _play_pre_break_chime(self):
        chime_played = False
        if self.settings.get("enable_sound"):
            try:
                import winsound
                sound_path = os.path.join(APP_ROOT, "resources", "on_pre_break.wav")
                if os.path.exists(sound_path):
                    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    chime_played = True
            except Exception as e:
                logger.error(f"Failed to play pre-break chime: {e}")
        
        delay_ms = 2000 if chime_played else 0
        if hasattr(self, "window") and self.window:
            self.window.after(delay_ms, self._play_break_audio)
        else:
            self._play_break_audio()

    def _create_overlay_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="black")
        self.window.overrideredirect(True)

        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.bind("<Escape>", lambda e: None)
        self.window.bind("<Alt-F4>", lambda e: None)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        self.window.geometry(f"{sw}x{sh}+0+0")
        self.window.grab_set()

        self._build_overlay_ui()

    def _build_overlay_ui(self):
        main_frame = tk.Frame(self.window, bg="black")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        type_text = "☕ Short Break" if self.break_type == "short" else "🧘 Long Break"
        tk.Label(
            main_frame,
            text=type_text,
            font=("Segoe UI", 20),
            fg=TH["accent"],
            bg="black",
        ).pack(pady=(0, 20))

        self._countdown_var = tk.StringVar(value=str(self.duration))
        tk.Label(
            main_frame,
            textvariable=self._countdown_var,
            font=("Segoe UI Light", 96, "bold"),
            fg="white",
            bg="black",
        ).pack(pady=(0, 20))

        self._breathing_var = tk.StringVar(value="Breathe In...")
        self._breathing_label = tk.Label(
            main_frame,
            textvariable=self._breathing_var,
            font=("Segoe UI", 24),
            fg=TH["fg_dim"],
            bg="black",
        )
        self._breathing_label.pack(pady=(0, 10))

        btn_frame = tk.Frame(main_frame, bg="black")
        btn_frame.pack(pady=10)

        btn_skip = tk.Button(
            btn_frame,
            text="Skip ⏭",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg=TH["fg_dim"],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["bg2"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._skip_break,
        )
        btn_skip.pack(side=tk.LEFT, padx=10)

        btn_postpone = tk.Button(
            btn_frame,
            text="Postpone (2m) ⏰",
            font=("Segoe UI", 12, "bold"),
            bg=TH["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=TH["accent_hover"],
            activeforeground="white",
            padx=20,
            pady=8,
            command=self._postpone_break,
        )
        btn_postpone.pack(side=tk.LEFT, padx=10)

        _add_hover(btn_skip, "#1a1a2e", TH["bg2"], TH["fg_dim"], "white")
        _add_hover(btn_postpone, TH["accent"], TH["accent_hover"])

        tk.Label(
            main_frame,
            text="Look away from the screen • Focus on something 20ft away",
            font=("Segoe UI", 12),
            fg="#444",
            bg="black",
        ).pack(pady=(20, 0))

    def _skip_break(self):
        self.status = "skipped"
        logger.info("Break skipped by user action.")
        self._cleanup()

    def _postpone_break(self):
        self.status = "postponed"
        logger.info("Break postponed by user action.")
        self._cleanup()

    def _restore(self):
        # Implement restore logic in case of failure or overlay close
        pass

    def _start_countdown(self):
        self._remaining = self.duration
        self._tick_countdown()

    def _tick_countdown(self):
        if self._remaining > 0:
            try:
                self._countdown_var.set(str(self._remaining))

                elapsed = self.duration - self._remaining
                delay = int(self.settings.get("voice_start_delay_sec", 3))

                if elapsed < delay:
                    self._breathing_var.set("Prepare to breathe... 🧘")
                    self._breathing_label.config(fg=TH["fg_dim"])
                else:
                    cycle_time = elapsed - delay
                    T = max(1, self._inhale_sec + self._hold_in_sec + self._exhale_sec + self._hold_out_sec)
                    cycle = cycle_time % T

                    if cycle < self._inhale_sec:
                        self._breathing_var.set("Breathe In... 🌬️")
                        self._breathing_label.config(fg=TH["success"])
                        if cycle == 0:
                            self._speak_phase(self.settings.get("voice_inhale_text", "Breathe in"))
                    elif cycle < self._inhale_sec + self._hold_in_sec:
                        self._breathing_var.set("Hold... 🛑")
                        self._breathing_label.config(fg=TH["warning"])
                        if cycle == self._inhale_sec:
                            self._speak_phase(self.settings.get("voice_hold_in_text", "Hold"))
                    elif cycle < self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                        self._breathing_var.set("Breathe Out... 💨")
                        self._breathing_label.config(fg=TH["accent"])
                        if cycle == self._inhale_sec + self._hold_in_sec:
                            self._speak_phase(self.settings.get("voice_exhale_text", "Breathe out"))
                    else:
                        self._breathing_var.set("Hold... 🛑")
                        self._breathing_label.config(fg=TH["fg_dim"])
                        if cycle == self._inhale_sec + self._hold_in_sec + self._exhale_sec:
                            self._speak_phase(self.settings.get("voice_hold_out_text", "Hold"))

                self._remaining -= 1
                self.window.after(1000, self._tick_countdown)
            except tk.TclError:
                pass
        else:
            self._cleanup()

    def _should_speak_voice(self) -> bool:
        if not self._voice_enabled:
            return False
        
        # Check break type filter
        vt = self.settings.get("voice_break_type", "Both")
        if vt == "Short Only" and self.break_type != "short":
            return False
        if vt == "Long Only" and self.break_type != "long":
            return False
            
        # Check duration threshold
        min_dur = int(self.settings.get("voice_min_duration_sec", 15))
        if self.duration < min_dur:
            return False
            
        return True

    def _speak_phase(self, text):
        if self._should_speak_voice():
            from core.audio import speak_sapi_async
            voice_name = self.settings.get("voice_name", "Default")
            volume = int(self.settings.get("voice_volume", 80))
            rate = int(self.settings.get("voice_rate", 0))
            pitch = int(self.settings.get("voice_pitch", 0))
            speak_sapi_async(text, voice_name, volume, rate, pitch)

    def _start_focus_keeper(self):
        self._keep_on_top()

    def _keep_on_top(self):
        if not hasattr(self, "window") or not self.window.winfo_exists():
            return
        try:
            if self.window.state() == "iconic":
                self.window.deiconify()

            self.window.lift()
            self.window.attributes("-topmost", True)

            if self.window.focus_displayof() is None:
                self._focus_fail_count += 1
                if self._focus_fail_count >= 5 and not self._using_windowed_fallback:
                    logger.warning(
                        "Focus repeatedly lost. Applying windowed borderless fallback..."
                    )
                    try:
                        self.window.attributes("-fullscreen", False)
                        self.window.overrideredirect(True)
                        sw = self.window.winfo_screenwidth()
                        sh = self.window.winfo_screenheight()
                        self.window.geometry(f"{sw}x{sh}+0+0")
                        self._using_windowed_fallback = True
                    except Exception as ex:
                        logger.error(f"Failed to apply borderless fallback: {ex}")

                self.window.focus_force()
                try:
                    self.window.grab_set()
                except Exception:
                    pass
            else:
                self._focus_fail_count = 0
        except Exception as e:
            logger.error(f"Keep on top error: {e}")

        self.window.after(500, self._keep_on_top)

    def _cleanup(self):
        """Clean up and restore system state."""
        try:
            # Auto-resume media that was playing right before the break
            try:
                get_media_controller().resume_paused_media()
                logger.info("Executed resume for paused media sessions on break end.")
            except Exception as e:
                logger.error(f"Error resuming media on break end: {e}")

            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            self.window.grab_release()
            self.window.destroy()

            if self.settings.get("enable_sound"):
                try:
                    import winsound

                    sound_path = os.path.join(
                        APP_ROOT, "resources", "on_stop_break.wav"
                    )
                    if os.path.exists(sound_path):
                        winsound.PlaySound(
                            sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
                        )
                except Exception:
                    pass
            if self.on_complete:
                self.on_complete(self.status)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
