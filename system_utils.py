import ctypes
import os


def is_system_awake_and_unlocked():
    """
    Returns True if the workstation is unlocked and active.
    If the system is locked, asleep, or the display is off in a secure way,
    OpenInputDesktop will typically fail.
    """
    if os.name != "nt":
        return True

    try:
        user32 = ctypes.windll.user32
        # 0x0100 = DESKTOP_READOBJECTS
        h_desktop = user32.OpenInputDesktop(0, False, 0x0100)
        if h_desktop:
            user32.CloseDesktop(h_desktop)
            return True
        return False
    except Exception:
        return False


def monitor_parent_process(quit_callback, check_interval_sec=5):
    """
    Spawns a background daemon thread that monitors the parent process.
    If the parent process was AeroHub and it exits/terminates, runs quit_callback.
    """
    import threading
    import time
    import sys
    import psutil
    import logging

    logger = logging.getLogger("AeroHub.ParentMonitor")
    
    parent_pid = os.getppid()
    parent_is_hub = False
    parent_create_time = None

    try:
        parent_proc = psutil.Process(parent_pid)
        parent_cmd = parent_proc.cmdline()
        parent_name = parent_proc.name().lower()
        if any("aerohub.py" in arg.lower() for arg in parent_cmd) or "pythonw_aerohub.exe" in parent_name:
            parent_is_hub = True
            parent_create_time = parent_proc.create_time()
            logger.info(f"Parent process is AeroHub (PID {parent_pid}, created at {parent_create_time})")
    except Exception as e:
        logger.warning(f"Failed to inspect parent process: {e}")

    if not parent_is_hub:
        logger.info("Parent process is not AeroHub. Running in standalone mode.")
        return

    def _monitor():
        while True:
            try:
                parent_proc = psutil.Process(parent_pid)
                if not parent_proc.is_running() or parent_proc.create_time() != parent_create_time or parent_proc.status() == psutil.STATUS_ZOMBIE:
                    logger.warning("Parent AeroHub process has terminated. Initiating shutdown.")
                    quit_callback()
                    break
            except psutil.NoSuchProcess:
                logger.warning("Parent AeroHub process has terminated (no such process). Initiating shutdown.")
                quit_callback()
                break
            except Exception as e:
                logger.error(f"Error checking parent process: {e}")
            time.sleep(check_interval_sec)

    thread = threading.Thread(target=_monitor, daemon=True)
    thread.start()

