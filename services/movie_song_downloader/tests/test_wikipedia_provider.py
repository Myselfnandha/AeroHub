import pytest
from unittest.mock import patch, MagicMock
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.wikipedia_provider import WikipediaProvider


@pytest.mark.asyncio
async def test_wikipedia_search():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = WikipediaProvider()

    mock_search_resp = {
        "query": {
            "search": [
                {
                    "title": "Vikram (2022 film)",
                    "snippet": (
                        "Vikram is a 2022 Indian Tamil-language action thriller film "
                        "directed by Lokesh Kanagaraj..."
                    ),
                    "pageid": 12345,
                }
            ]
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_search_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        results = await provider.search("Vikram", year=2022)
        assert len(results) > 0
        assert results[0].title == "Vikram"
        assert results[0].year == 2022
        assert results[0].source == "wikipedia"
        assert results[0].source_id == "12345"


@pytest.mark.asyncio
async def test_wikipedia_get_details():
    await db.run_migrations()
    provider = WikipediaProvider()

    mock_details_resp = {
        "query": {
            "pages": {
                "12345": {
                    "title": "Vikram (2022 film)",
                    "thumbnail": {"source": "https://image.xyz/vikram.jpg"},
                    "extract": (
                        "Vikram is a 2022 action thriller..."
                    ),
                }
            }
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_details_resp

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie = await provider.get_movie_details("12345")
        assert movie is not None
        assert movie.title == "Vikram"
        assert movie.year == 2022
        assert movie.poster_url == "https://image.xyz/vikram.jpg"
        assert "action thriller" in movie.overview
