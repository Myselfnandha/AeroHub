import re

with open("services/media_control/media_control.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove MediaDashboard class completely
content = re.sub(
    r"class MediaDashboard:.*?# ══════════════════════════════════════════════════════════\n",
    "# ══════════════════════════════════════════════════════════\n",
    content,
    flags=re.DOTALL,
)

# 2. Remove self.root and self.dashboard initialization
init_target = """        # Initialize Tkinter root for dashboard on main thread
        self.root = tk.Tk()
        self.root.withdraw()
        self.dashboard = MediaDashboard(self, self.root)
        """
content = content.replace(init_target, "")

# 3. Clean _handle_window_msg dashboard toggle
handle_msg_target = """                    # Only the Play/Pause button (id=2) opens the dashboard on multi-session
                    if wparam == 2 and count > 1:
                        logger.info("Multi-session detected on Play/Pause click — toggling dashboard...")
                        self.root.after(0, self.dashboard.toggle)
                    else:
                        logger.info("Executing standard media key command...")
                        for ctrl in self.controls:
                            if ctrl["id"] == wparam:
                                ctrl["cmd"]()
                                break"""
handle_msg_replacement = """                    logger.info("Executing standard media key command...")
                    for ctrl in self.controls:
                        if ctrl["id"] == wparam:
                            ctrl["cmd"]()
                            break"""
content = content.replace(handle_msg_target, handle_msg_replacement)

# 4. Clean show_context_menu
menu_target = """        win32gui.AppendMenu(hmenu, win32con.MF_STRING, DASHBOARD_CMD_ID, "Open Dashboard")
        win32gui.AppendMenu(hmenu, win32con.MF_SEPARATOR, 0, "")
        win32gui.AppendMenu(hmenu, win32con.MF_STRING, EXIT_CMD_ID, "Exit")"""
menu_replacement = (
    """        win32gui.AppendMenu(hmenu, win32con.MF_STRING, EXIT_CMD_ID, "Exit")"""
)
content = content.replace(menu_target, menu_replacement)

# 5. Clean WM_COMMAND
cmd_target = """            elif msg == win32con.WM_COMMAND:
                if wparam == EXIT_CMD_ID:
                    self.quit_app()
                elif wparam == DASHBOARD_CMD_ID:
                    self.root.after(0, self.dashboard.show)"""
cmd_replacement = """            elif msg == win32con.WM_COMMAND:
                if wparam == EXIT_CMD_ID:
                    self.quit_app()"""
content = content.replace(cmd_target, cmd_replacement)

# 6. Clean monitor_media dashboard updates
monitor_target = """                if new_count != getattr(self, 'prev_active_count', -1):
                    logger.info(f"Active sessions count changed to: {new_count}")
                    prev_count = getattr(self, 'prev_active_count', -1)
                    # Auto-show dashboard when going from 1 to >1 session, but NOT on startup
                    if prev_count != -1 and new_count > 1 and prev_count <= 1:
                        if not self.dashboard._visible:
                            logger.info("Auto-opening dashboard due to multiple sessions")
                            self.root.after(0, self.dashboard.show)
                    self.prev_active_count = new_count

                # Generate a simple hash of the current session state to avoid unnecessary UI rebuilds
                current_state_hash = str([{
                    "id": d["app_id"],
                    "status": d["status"],
                    "title": d["title"],
                    "artist": d["artist"]
                } for d in active_sessions_list])

                if current_state_hash != getattr(self, 'prev_state_hash', ""):
                    # ALWAYS send data to dashboard so it has a cached copy to display instantly on toggle
                    self.root.after(0, self.dashboard.update_sessions, active_sessions_list)
                    self.prev_state_hash = current_state_hash"""
monitor_replacement = """                if new_count != getattr(self, 'prev_active_count', -1):
                    logger.info(f"Active sessions count changed to: {new_count}")
                    self.prev_active_count = new_count"""
content = content.replace(monitor_target, monitor_replacement)

# 7. Replace run() loop
run_target = """    def run(self):
        self.root.mainloop()"""
run_replacement = """    def run(self):
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.quit_app()"""
content = content.replace(run_target, run_replacement)

with open("services/media_control/media_control.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patch applied successfully")
