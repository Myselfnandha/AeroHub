import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
from movie_song_downloader.core.database import db
from movie_song_downloader.core.models import Movie
from movie_song_downloader.core.settings_manager import settings_manager
from movie_song_downloader.services.movie_service import MovieService


@pytest.mark.asyncio
async def test_get_today_releases_fresh_fetch():
    # Arrange: Ensure migrations are run and settings/movies are clean
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    await settings_manager.set("last_fetch_date", "2000-01-01")  # Outdated date
    await settings_manager.set(
        "scraping_limit", "0"
    )  # Avoid OMDb enrichment calls for stubs in this test

    mock_movie = Movie(
        tmdb_id=123,
        source="wikipedia",
        source_id="p123",
        title="Test Movie 2026",
        year=datetime.date.today().year,
        poster_url="http://example.com/poster.jpg",
    )

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(return_value=[mock_movie])

    service = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service.get_today_releases("IN")

    # Assert
    assert len(movies) == 1
    assert movies[0].title == "Test Movie 2026"
    wiki_mock.get_today_releases.assert_called_once_with(region="IN")

    # Check that settings updated the date
    saved_date = await settings_manager.get("last_fetch_date")
    assert saved_date == datetime.date.today().isoformat()


@pytest.mark.asyncio
async def test_get_today_releases_from_cache():
    # Arrange: Populate DB and update last_fetch_date to today
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    current_date_str = datetime.date.today().isoformat()
    await settings_manager.set("last_fetch_date", current_date_str)

    # Seed a cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=456,
        source="wikipedia",
        source_id="p456",
        title="Cached Movie 2026",
        year=current_year,
        poster_url="http://example.com/cached.jpg",
        release_date=current_date_str,
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock()

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should load directly from DB cache, meaning wiki_provider is not called
    assert len(movies) == 1
    assert movies[0].title == "Cached Movie 2026"
    wiki_mock.get_today_releases.assert_not_called()


@pytest.mark.asyncio
async def test_get_today_releases_fallback_on_failure():
    # Arrange: Populate DB but set last_fetch_date to outdated
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM settings")
        await conn.execute("DELETE FROM movies")
        await conn.commit()
    finally:
        await conn.close()

    current_year = datetime.date.today().year
    await settings_manager.set("last_fetch_date", "2000-01-01")

    # Seed older cached movie
    service = MovieService()
    cached_movie = Movie(
        tmdb_id=789,
        source="wikipedia",
        source_id="p789",
        title="Fallback Movie 2026",
        year=current_year,
        poster_url="http://example.com/fallback.jpg",
        release_date="2026-01-01",
    )
    await service._db_save_movie_album_tracks(cached_movie, None, [])

    # Mock wiki provider to raise an exception
    wiki_mock = MagicMock()
    wiki_mock.get_today_releases = AsyncMock(side_effect=Exception("Network error"))

    service_with_mock = MovieService(wiki_provider=wiki_mock)

    # Act
    movies = await service_with_mock.get_today_releases("IN")

    # Assert: Should gracefully fallback to DB cache
    assert len(movies) == 1
    assert movies[0].title == "Fallback Movie 2026"
    wiki_mock.get_today_releases.assert_called_once()
