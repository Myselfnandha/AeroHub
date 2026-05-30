"""
Quick diagnostic: enumerate all media sessions and print their status.
Run this while playing audio in 2+ apps to see what Windows reports.
"""
import asyncio
import ctypes

from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as SessionManager
)

# Init COM as MTA
ctypes.windll.ole32.CoInitializeEx(None, 2)

STATUS_MAP = {
    0: "Closed",
    1: "Opened",
    2: "Changing",
    3: "Stopped",
    4: "Playing",
    5: "Paused",
}

async def main():
    manager = await SessionManager.request_async()
    
    print("=" * 60)
    print("CURRENT SESSION:")
    current = manager.get_current_session()
    if current:
        info = current.get_playback_info()
        status = info.playback_status if info else None
        try:
            props = await current.try_get_media_properties_async()
            title = props.title if props else ""
            artist = props.artist if props else ""
        except Exception:
            title = artist = "?"
        app_id = current.source_app_user_model_id
        print(f"  App: {app_id}")
        print(f"  Status: {status} ({STATUS_MAP.get(status, 'Unknown')})")
        print(f"  Title: {title}")
        print(f"  Artist: {artist}")
    else:
        print("  (none)")
    
    print()
    print("ALL SESSIONS:")
    sessions = manager.get_sessions()
    total = 0
    for i, s in enumerate(sessions):
        total += 1
        try:
            s_info = s.get_playback_info()
            s_status = s_info.playback_status if s_info else None
            try:
                s_props = await s.try_get_media_properties_async()
                s_title = s_props.title if s_props else ""
                s_artist = s_props.artist if s_props else ""
            except Exception:
                s_title = s_artist = "?"
            s_app_id = s.source_app_user_model_id
            print(f"  [{i}] App: {s_app_id}")
            print(f"      Status: {s_status} ({STATUS_MAP.get(s_status, 'Unknown')})")
            print(f"      Title: {s_title}")
            print(f"      Artist: {s_artist}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")
    
    if total == 0:
        print("  (none)")
    
    print(f"\nTotal sessions: {total}")
    print(f"Playing/Paused only: {sum(1 for s in sessions if s.get_playback_info() and s.get_playback_info().playback_status in (4,5))}")
    print("=" * 60)

asyncio.run(main())
