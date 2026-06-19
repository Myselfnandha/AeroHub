import pytest
import json
from unittest.mock import patch, MagicMock
from movie_song_downloader.providers.spotify_provider import SpotifyProvider


@pytest.mark.asyncio
async def test_get_spotify_album():
    provider = SpotifyProvider()

    # Mock embed page HTML response for album
    mock_entity = {
        "type": "album",
        "title": "Ponniyin Selvan - Original Score",
        "subtitle": "A.R. Rahman",
        "id": "7y3bI6blXr4I8l4kKGcBfE",
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/cover_small.jpg",
                    "maxHeight": 300,
                    "maxWidth": 300,
                },
                {
                    "url": "https://image.xyz/cover_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                },
            ]
        },
        "trackList": [
            {
                "uri": "spotify:track:1nHTOlxSEyyrLH6wzzMJTd",
                "title": "Armageddon",
                "subtitle": "A.R. Rahman",
                "duration": 269000,
                "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
            },
            {
                "uri": "spotify:track:2nHTOlxSEyyrLH6wzzMJTz",
                "title": "Solaikuyil",
                "subtitle": "A.R. Rahman, Shreya Ghoshal",
                "duration": 310000,
                "audioPreview": None,
            },
        ],
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/album/7y3bI6blXr4I8l4kKGcBfE"
        )

        # Verify Movie
        assert movie.source == "spotify"
        assert movie.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert movie.title == "Ponniyin Selvan - Original Score"
        assert movie.poster_url == "https://image.xyz/cover_large.jpg"

        # Verify Album
        assert album.source == "spotify"
        assert album.source_id == "7y3bI6blXr4I8l4kKGcBfE"
        assert album.title == "Ponniyin Selvan - Original Score"
        assert album.artist == "A.R. Rahman"
        assert album.cover_url == "https://image.xyz/cover_large.jpg"
        assert album.total_tracks == 2

        # Verify Tracks
        assert len(tracks) == 2
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].duration_ms == 269000
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"

        assert tracks[1].title == "Solaikuyil"
        assert tracks[1].artist == "A.R. Rahman, Shreya Ghoshal"
        assert tracks[1].source_id == "2nHTOlxSEyyrLH6wzzMJTz"
        assert tracks[1].track_number == 2
        assert tracks[1].preview_url is None


@pytest.mark.asyncio
async def test_get_spotify_track():
    provider = SpotifyProvider()

    # Mock embed page HTML response for track
    mock_entity = {
        "type": "track",
        "title": "Armageddon",
        "name": "Armageddon",
        "id": "1nHTOlxSEyyrLH6wzzMJTd",
        "artists": [{"name": "A.R. Rahman"}],
        "duration": 269000,
        "visualIdentity": {
            "image": [
                {
                    "url": "https://image.xyz/track_large.jpg",
                    "maxHeight": 640,
                    "maxWidth": 640,
                }
            ]
        },
        "audioPreview": {"url": "https://preview.xyz/track1.mp3"},
    }

    mock_state_data = {
        "props": {"pageProps": {"state": {"data": {"entity": mock_entity}}}}
    }

    mock_html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(mock_state_data)
        + "</script></body></html>"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        movie, album, tracks = await provider.get_spotify_album_or_track(
            "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"
        )

        # Verify single wrapped track
        assert movie.title == "Armageddon"
        assert movie.poster_url == "https://image.xyz/track_large.jpg"

        assert album.title == "Armageddon"
        assert album.artist == "A.R. Rahman"
        assert album.total_tracks == 1

        assert len(tracks) == 1
        assert tracks[0].title == "Armageddon"
        assert tracks[0].artist == "A.R. Rahman"
        assert tracks[0].source_id == "1nHTOlxSEyyrLH6wzzMJTd"
        assert tracks[0].track_number == 1
        assert tracks[0].preview_url == "https://preview.xyz/track1.mp3"
