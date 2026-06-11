import pytest
import asyncio
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider


def test_lyrics_sync_detection():
    provider = LyricsProvider()

    synced_text = (
        "[00:12.34] Synced line one\n"
        "[00:15.50] Synced line two\n"
        "[00:19.00] Synced line three\n"
    )

    plain_text = "This is line one\nThis is line two\nThis is line three\n"

    # Check regex sync detection
    assert provider._is_synced(synced_text) is True
    assert provider._is_synced(plain_text) is False
    assert provider._is_synced("") is False


@pytest.mark.asyncio
async def test_waterfall_priority_fallback(monkeypatch):
    provider = LyricsProvider()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        return '["lrclib", "genius"]'  # Custom waterfall subset

    monkeypatch.setattr(settings_manager, "get", mock_get)

    calls = []

    # Mock thread executor helper _sync_search_task
    async def mock_thread(func, *args):
        # args[0] is search_query, args[1] is provider
        provider_name = args[1]
        calls.append(provider_name)
        if provider_name == "lrclib":
            return None  # Simulate miss
        elif provider_name == "genius":
            return "Genius plain text lyrics content"  # Simulate hit
        return None

    monkeypatch.setattr(asyncio, "to_thread", mock_thread)

    lyrics, lyrics_type = await provider.fetch("Title", "Artist")

    # Verify both providers were queried in sequence
    assert "lrclib" in calls
    assert "genius" in calls
    assert lyrics == "Genius plain text lyrics content"
    assert lyrics_type == "plain"
