import pytest
from unittest.mock import patch
from MovieSongDownloader.providers.musicbrainz_provider import MusicBrainzProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.core.database import db


@pytest.mark.asyncio
async def test_musicbrainz_enrich_album():
    await db.run_migrations()
    provider = MusicBrainzProvider()

    # Mock album and tracks
    album = Album(title="Vikram", artist="Anirudh Ravichander")
    tracks = [Track(title="Pathala Pathala"), Track(title="Wasted")]

    # Mock search response
    mock_search = {
        "release-groups": [
            {
                "id": "rg_123",
                "title": "Vikram",
                "artist-credit": [{"artist": {"name": "Anirudh Ravichander"}}],
            }
        ]
    }

    # Mock browse response containing tracks and ISRCs
    mock_browse = {
        "releases": [
            {
                "title": "Vikram",
                "id": "rel_456",
                "media": [
                    {
                        "tracks": [
                            {
                                "title": "Pathala Pathala",
                                "recording": {"isrcs": ["IN-A23-22-00001"]},
                            },
                            {
                                "title": "Wasted",
                                "recording": {"isrcs": ["IN-A23-22-00002"]},
                            },
                        ]
                    }
                ],
            }
        ]
    }

    async def mock_mb_req_handler(url, params):
        if "release-group" in url:
            return mock_search
        elif "release" in url:
            return mock_browse
        return None

    with patch.object(provider, "_mb_request", side_effect=mock_mb_req_handler):
        composer, isrc_map = await provider.enrich_album(album, tracks)
        assert composer == "Anirudh Ravichander"
        assert len(isrc_map) == 2
        assert isrc_map["Pathala Pathala"] == "IN-A23-22-00001"
        assert isrc_map["Wasted"] == "IN-A23-22-00002"
