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
        self._paused_app_ids = []
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
        """Pause all currently PLAYING media sessions. Records app_ids to resume later."""
        with self._lock:
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        paused_ids = self._run_async(self._do_pause())
        if paused_ids is None:
            # Async failed — fall back to global media key
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        with self._lock:
            self._paused_app_ids = paused_ids

        logger.info(f"Paused {len(paused_ids)} active media sessions via winsdk.")

    def resume_paused_media(self):
        """Resume only the media sessions that were paused before the break."""
        with self._lock:
            ids_to_resume = list(self._paused_app_ids)
            self._paused_app_ids.clear()

        if not WINSDK_AVAILABLE:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        if not ids_to_resume:
            return

        count = self._run_async(self._do_resume(ids_to_resume))
        if count is None:
            _send_media_key(VK_MEDIA_PLAY_PAUSE)
            return

        logger.info(f"Resumed {count} media sessions via winsdk.")

    async def _do_pause(self):
        """Fetch fresh sessions and pause all that are Playing (status==4).

        Returns list of app_ids that were successfully paused.
        Deduplicates by app_id so Chrome with 2 tabs only gets paused once.
        """
        paused_ids = []
        seen_app_ids = set()

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""

                    # Deduplicate: only process first session per app
                    if app_id in seen_app_ids:
                        continue
                    seen_app_ids.add(app_id)

                    info = session.get_playback_info()
                    if not info:
                        continue

                    status = info.playback_status
                    if status != 4:  # Not Playing
                        continue

                    result = await session.try_pause_async()
                    if result:
                        paused_ids.append(app_id)
                    else:
                        # try_pause_async returned False — session may not support it
                        paused_ids.append(app_id)

                except Exception as e:
                    logger.debug(f"Error pausing session ({app_id}): {e}")
                    continue

        except Exception as e:
            logger.error(f"SessionManager pause error: {e}")

        return paused_ids

    async def _do_resume(self, app_ids_to_resume):
        """Fetch fresh sessions and resume those whose app_id is in the list.

        Uses fresh session objects (never stale references).
        """
        resumed = 0
        target_ids = set(app_ids_to_resume)

        try:
            manager = await SessionManager.request_async()
            sessions = manager.get_sessions()

            for session in sessions:
                try:
                    app_id = session.source_app_user_model_id or ""
                    if app_id not in target_ids:
                        continue

                    # Remove so we only resume once per app
                    target_ids.discard(app_id)

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
