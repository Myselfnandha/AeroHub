import pytest
from MovieSongDownloader.services.folder_service import FolderService
from MovieSongDownloader.core.models import Movie, Album, Track


def test_sanitize_name():
    # Remove Windows invalid characters
    assert (
        FolderService.sanitize_name("Leo: Naan Ready? *FLAC*")
        == "Leo- Naan Ready- -FLAC-"
    )
    assert FolderService.sanitize_name("Artist / Title") == "Artist - Title"
    assert FolderService.sanitize_name("") == "Unknown"


@pytest.mark.asyncio
async def test_target_path_generation(monkeypatch):
    service = FolderService()

    # Mock settings manager keys
    from MovieSongDownloader.core.settings_manager import settings_manager

    async def mock_get(key):
        if key == "output_dir":
            return "C:/Downloads"
        elif key == "folder_format":
            return "{Year}/{Movie}/Songs"
        elif key == "filename_format":
            return "{TrackNum} - {Title}"
        return ""

    monkeypatch.setattr(settings_manager, "get", mock_get)

    movie = Movie(title="Inception", year=2010)
    album = Album(title="Inception OST")
    track = Track(title="Time", track_number=5, artist="Hans Zimmer")

    target_dir, file_path = await service.get_target_path(movie, album, track, "mp3")

    # Verify proper replacements and path construction
    assert (
        "C:\\Downloads\\2010\\Inception\\Songs" in target_dir
        or "C:/Downloads/2010/Inception/Songs" in target_dir
    )
    assert "05 - Time.mp3" in file_path
