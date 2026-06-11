import win32gui
import win32con
import win32process


def pause_app(process_name):
    # Find HWNDs for process
    hwnds = []

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            hwnds.append((hwnd, pid))
        return True

    win32gui.EnumWindows(callback, hwnds)

    import psutil

    target_pids = [
        p.pid
        for p in psutil.process_iter(["name"])
        if p.info["name"] and p.info["name"].lower() == process_name.lower()
    ]

    for hwnd, pid in hwnds:
        if pid in target_pids:
            print(f"Sending APPCOMMAND_MEDIA_PAUSE to {process_name} (HWND: {hwnd})")
            win32gui.PostMessage(
                hwnd, win32con.WM_APPCOMMAND, 0, win32con.APPCOMMAND_MEDIA_PAUSE << 16
            )
            # or try PLAY_PAUSE
            # win32gui.PostMessage(hwnd, win32con.WM_APPCOMMAND, 0, win32con.APPCOMMAND_MEDIA_PLAY_PAUSE << 16)


if __name__ == "__main__":
    pause_app("vlc.exe")
    pause_app("firefox.exe")
