import pytest
from unittest.mock import patch
from MovieSongDownloader.core.database import db
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider


@pytest.mark.asyncio
async def test_jiosaavn_search_album():
    await db.run_migrations()

    # Mock DB cache clear
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM api_cache")
        await conn.commit()
    finally:
        await conn.close()

    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's search_albums call
    mock_albums = [
        {
            "album_id": "alb_123",
            "title": "Vikram",
            "artists": "Anirudh Ravichander",
            "track_count": 5,
            "thumbnails": {"quality": {"500x500": "https://images.xyz/vikram_500.jpg"}},
        }
    ]

    with patch.object(
        provider._client, "search_albums", return_value=mock_albums
    ) as mock_search:
        albums = await provider.get_soundtrack("Vikram", 2022)
        assert len(albums) == 1
        assert albums[0].source == "jiosaavn"
        assert albums[0].source_id == "alb_123"
        assert albums[0].title == "Vikram"
        assert albums[0].artist == "Anirudh Ravichander"
        assert albums[0].cover_url == "https://images.xyz/vikram_500.jpg"
        mock_search.assert_called_once_with("Vikram 2022", limit=8)


@pytest.mark.asyncio
async def test_jiosaavn_get_tracks():
    await db.run_migrations()
    provider = JioSaavnProvider()

    # Mock the JioSaavn SDK's album_info call
    mock_info = {
        "album_id": "alb_123",
        "title": "Vikram",
        "tracks": [
            {
                "track_id": "trk_999",
                "title": "Pathala Pathala",
                "primary_artists": "Anirudh Ravichander, Kamal Haasan",
                "duration": 210,
                "stream_urls": {
                    "very_high_quality": "https://stream.xyz/pathala_320.mp3",
                    "low_quality": "https://stream.xyz/pathala_96.mp3",
                },
            }
        ],
    }

    with patch.object(
        provider._client, "album_info", return_value=mock_info
    ) as mock_info_call:
        tracks = await provider.get_tracks("alb_123")
        assert len(tracks) == 1
        assert tracks[0].source == "jiosaavn"
        assert tracks[0].source_id == "trk_999"
        assert tracks[0].title == "Pathala Pathala"
        assert tracks[0].artist == "Anirudh Ravichander, Kamal Haasan"
        assert tracks[0].duration_ms == 210000
        assert tracks[0].download_url == "https://stream.xyz/pathala_320.mp3"
        mock_info_call.assert_called_once_with("alb_123")
