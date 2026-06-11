import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.core.models import Movie
from MovieSongDownloader.providers.omdb_provider import OMDbProvider


@pytest.mark.asyncio
async def test_omdb_enrich_movie():
    await db.run_migrations()

    # Seed API key setting
    await settings_manager.set("omdb_api_key", "test_key")

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = OMDbProvider()

    # Un-enriched movie with empty source_id (should be enriched with imdbID)
    movie = Movie(source="wikipedia", source_id="", title="Vikram", year=2022)

    mock_omdb_resp = {
        "Response": "True",
        "Title": "Vikram",
        "Year": "2022",
        "imdbID": "tt1234567",
        "imdbRating": "8.3",
        "Actors": "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil",
        "Plot": "A special agent investigates a case of serial killings...",
        "Genre": "Action, Thriller",
        "Language": "Tamil",
        "Poster": "https://image.xyz/poster.jpg",
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_omdb_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched = await provider.enrich_movie(movie)
        assert enriched.rating == "8.3"
        assert enriched.cast_info == "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil"
        assert enriched.poster_url == "https://image.xyz/poster.jpg"
        assert "special agent" in enriched.overview
        assert "Action" in enriched.genres
        assert enriched.language == "Tamil"
        # Since source_id was empty, it should be set to imdbID
        assert enriched.source_id == "tt1234567"

    # Test that pre-populated source_id is not overwritten
    movie_with_id = Movie(
        source="wikipedia", source_id="12345", title="Vikram", year=2022
    )
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        enriched_with_id = await provider.enrich_movie(movie_with_id)
        assert enriched_with_id.source_id == "12345"
