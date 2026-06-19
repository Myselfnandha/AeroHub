import ctypes
import ctypes.wintypes
import threading
import asyncio
import time
from core.logger import logger
from core.constants import (
    VK_MEDIA_PLAY_PAUSE,
    KEYEVENTF_EXTENDEDKEY,
    KEYEVENTF_KEYUP,
)

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as SessionManager,
    )
    WINSDK_AVAILABLE = True
except ImportError:
    WINSDK_AVAILABLE = False


class MediaController:
    """Manages media pause/resume on a single dedicated COM+async thread.

    Fixes:
    - No more asyncio.run() per call (which creates/destroys event loops)
    - COM is initialized once on the dedicated thread
    - Stale session objects are never reused across calls
    - Each pause/resume fetches fresh sessions from the SessionManager
    - Deduplicates sessions by app_id to prevent flicker
    - Robust error handling per-session so one bad session doesn't crash all
    """

    def __init__(self):
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._paused_sessions = []
        self._lock = threading.Lock()
        self._start_thread()

    def _start_thread(self):
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)

    def _run_loop(self):
        # Initialize COM as MTA once for the lifetime of this thread
        hr = ctypes.windll.ole32.CoInitializeEx(None, 2)
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._ready.set()
            self._loop.run_forever()
        finally:
            if hr in (0, 1):
                ctypes.windll.ole32.CoUninitialize()

    def _run_async(self, coro):
        """Schedule a coroutine on the dedicated loop and wait for result."""
        if not self._loop or not self._loop.is_running():
            return None
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout=10)
        except Exception as e:
            logger.error(f"MediaController async error: {e}")
            return None

    def pause_active_media(self):
        """Pause all currently PLAYING media sessions. Records (app_id, title) to resume later."""
        with self._lock:
            self._paused_sessions.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        paused = self._run_async(self._do_pause())
        if paused is None:
            # Async failed — fall back to global media key
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        with self._lock:
            self._paused_sessions = paused

        logger.info(f"Paused {len(paused)} active media sessions via winsdk.")

    def resume_paused_media(self):
        """Resume only the media sessions that were paused before the break."""
        with self._lock:
            sessions_to_resume = list(self._paused_sessions)
            self._paused_sessions.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        if not sessions_to_resume:
            return

        count = self._run_async(self._do_resume(sessions_to_resume))
        if count is None:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        logger.info(f"Resumed {count} media sessions via winsdk.")

    async def _do_pause(self):
        """Fetch fresh sessions and pause all that are Playing (status==4).

        Returns list of (app_id, title) tuples that were successfully paused.
        """
        paused = []
        seen_sessions = set()

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    
                    title = ""
                    try:
                        props = await session.try_get_media_properties_async()
                        title = props.title or ""
                    except Exception:
                        pass

                    # Unique session key
                    s_key = (app_id, title)
                    if s_key in seen_sessions:
                        continue
                    seen_sessions.add(s_key)

                    info = session.get_playback_info()
                    if not info:
                        continue

                    status = info.playback_status
                    if status != 4:  # Not Playing
                        continue

                    result = await session.try_pause_async()
                    # Keep track of it as paused
                    paused.append((app_id, title))

                except Exception as e:
                    logger.debug(f"Error pausing session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager pause error: {e}")

        return paused

    async def _do_resume(self, paused_sessions):
        """Fetch fresh sessions and resume those whose (app_id, title) matches the saved sessions.

        Uses fresh session objects.
        """
        resumed = 0
        targets = list(paused_sessions)

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    
                    title = ""
                    try:
                        props = await session.try_get_media_properties_async()
                        title = props.title or ""
                    except Exception:
                        pass

                    matched_target = None
                    for t in targets:
                        t_app_id, t_title = t
                        if t_app_id == app_id and (not t_title or t_title == title):
                            matched_target = t
                            break

                    if matched_target:
                        targets.remove(matched_target)
                        await session.try_play_async()
                        resumed += 1

                except Exception as e:
                    logger.debug(f"Error resuming session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager resume error: {e}")

        return resumed


def _send_media_key(vk_code: int):
    """Send a media key press/release via keybd_event (global fallback)."""
    try:
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(
            vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0
        )
        time.sleep(0.15)
    except Exception as e:
        logger.error(f"Media key send error: {e}")


# ── Singleton media controller ──
_media_controller = None


def get_media_controller():
    global _media_controller
    if _media_controller is None:
        _media_controller = MediaController()
    return _media_controller
