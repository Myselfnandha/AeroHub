"""
Singleton mutex — prevents running two instances of the same module.

Uses Windows named mutex via kernel32 on Windows, and fcntl file locking
on Linux / macOS.

Usage:
    from common.singleton import acquire_mutex
    if not acquire_mutex("AeroHub_BatteryMonitor"):
        sys.exit(0)  # Another instance is already running
"""

import os
import sys
import tempfile

# Keep file descriptor open for process lifetime on POSIX
_lock_fds: dict[str, int] = {}


def acquire_mutex(name: str) -> bool:
    """Try to acquire a named mutex/lock. Returns True if this is the first instance."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            ERROR_ALREADY_EXISTS = 183

            # CreateMutexW(lpMutexAttributes, bInitialOwner, lpName)
            mutex = kernel32.CreateMutexW(None, True, name)
            if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
                kernel32.CloseHandle(mutex)
                return False
            return True
        except Exception:
            return True
    else:
        # Linux / macOS: Use fcntl file locking
        try:
            import fcntl
            safe_name = os.path.basename(name)
            lock_dir = os.path.join(tempfile.gettempdir(), "aerohub_locks")
            os.makedirs(lock_dir, exist_ok=True)
            lock_file = os.path.join(lock_dir, f"{safe_name}.lock")
            if os.path.islink(lock_file):
                return False

            flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(lock_file, flags, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                _lock_fds[name] = fd
                return True
            except (BlockingIOError, OSError):
                os.close(fd)
                return False
        except Exception:
            return True

