import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider


@pytest.mark.asyncio
async def test_resolve_spotify_url():
    provider = SpotiFLACProvider()

    # Mock DDG HTML response containing track url
    mock_html = '<html><body><a href="https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd">Link</a></body></html>'
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        url = await provider._resolve_spotify_url("Armageddon", "A.R. Rahman")
        assert url == "https://open.spotify.com/track/1nHTOlxSEyyrLH6wzzMJTd"


@pytest.mark.asyncio
async def test_spotiflac_download():
    provider = SpotiFLACProvider()

    track = Track(
        source="spotify",
        source_id="1nHTOlxSEyyrLH6wzzMJTd",
        title="Armageddon",
        artist="A.R. Rahman",
        track_number=1,
    )

    # Mock settings_manager.get
    async def mock_settings_get(key):
        if key == "deezer_arl":
            return "test_arl"
        return None

    # Mock subprocess execution
    mock_process = AsyncMock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b"Downloaded successfully", b"")

    # Mock os.walk and file creation
    temp_file_created = None

    def mock_walk(top, topdown=True, onerror=None, followlinks=False):
        nonlocal temp_file_created
        # Create a mock file in the temp subfolder to simulate download
        # Top is output_dir/spotiflac_temp_1nHTOlxSEyyrLH6wzzMJTd
        temp_file_created = os.path.join(top, "track1.flac")
        os.makedirs(top, exist_ok=True)
        with open(temp_file_created, "w") as f:
            f.write("mock audio data")
        return [(top, [], ["track1.flac"])]

    # Mock _transcode_audio to avoid actual ffmpeg running
    async def mock_transcode(input_path, output_path, format_str, bitrate):
        with open(output_path, "w") as f:
            f.write("mock transcoded audio")

    # Mock shutil.move
    def mock_move(src, dst):
        with open(dst, "w") as f:
            f.write("mock final file")

    with (
        patch(
            "MovieSongDownloader.providers.spotiflac_provider.settings_manager.get",
            side_effect=mock_settings_get,
        ),
        patch("asyncio.create_subprocess_exec", return_value=mock_process),
        patch("os.walk", side_effect=mock_walk),
        patch.object(provider, "_transcode_audio", side_effect=mock_transcode),
        patch("shutil.move", side_effect=mock_move),
        patch("shutil.rmtree"),
    ):
        result_path = await provider.download(
            track=track, format="mp3", output_dir="./test_output", filename_template=""
        )

        assert "spotiflac_result_1nHTOlxSEyyrLH6wzzMJTd.mp3" in result_path
