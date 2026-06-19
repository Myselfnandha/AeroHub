import pytest
from movie_song_downloader.core.database import db
from movie_song_downloader.core.cache_manager import download_cache, api_cache


@pytest.mark.asyncio
async def test_api_cache_operations():
    # Force initialization first
    await db.run_migrations()

    key = "test_spotify_endpoint"
    payload = {"data": [1, 2, 3]}

    # Check cache miss
    miss = await api_cache.get(key)
    assert miss is None

    # Save cache with 5 seconds expiry
    await api_cache.set(key, "spotify", payload, expires_in_seconds=5)

    # Check cache hit
    hit = await api_cache.get(key)
    assert hit == payload

    # Save cache with -1 seconds expiry (expired)
    await api_cache.set(key, "spotify", payload, expires_in_seconds=-1)

    # Check cache expired (should return None)
    expired = await api_cache.get(key)
    assert expired is None


@pytest.mark.asyncio
async def test_download_cache_hash():
    h1 = download_cache.generate_hash("Artist", "Song", "Album", 200000)
    h2 = download_cache.generate_hash("artist", "song", "album", 200000)

    # Check case-insensitivity
    assert h1 == h2
