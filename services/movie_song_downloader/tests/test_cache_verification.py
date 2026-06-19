import pytest
from movie_song_downloader.core.database import db
from movie_song_downloader.core.cache_manager import api_cache


@pytest.mark.asyncio
async def test_cache_verification_logic():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    cache_key = "test_verification_key"
    cached_data = {
        "id": "123",
        "title": "Old Title",
        "rating": "7.5",
        "cast": "Old Cast",
    }

    # Verify when cache is empty, returns new data directly
    result = await api_cache.verify_scraped_data(
        cache_key, cached_data, ["rating", "cast"]
    )
    assert result == cached_data

    # Set initial cache
    await api_cache.set(cache_key, "test", cached_data)

    new_data = {"id": "456", "title": "New Title", "rating": "8.5", "cast": "New Cast"}

    # Verify fields (volatile fields rating/cast are updated, but id/title are kept from cached_data)
    result = await api_cache.verify_scraped_data(
        cache_key, new_data, ["rating", "cast"]
    )
    assert result["id"] == "123"
    assert result["title"] == "Old Title"
    assert result["rating"] == "8.5"
    assert result["cast"] == "New Cast"
