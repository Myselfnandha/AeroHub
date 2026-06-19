import pytest
from movie_song_downloader.services.folder_service import FolderService
from movie_song_downloader.core.models import Movie, Album, Track


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
    import movie_song_downloader.services.folder_service as fs_mod1
    try:
        import movie_song_downloader.services.folder_service as fs_mod2
    except ImportError:
        fs_mod2 = None

    async def mock_get(key):
        if key == "output_dir":
            return "C:/Downloads"
        elif key == "folder_format":
            return "{Year}/{Movie}/Songs"
        elif key == "filename_format":
            return "{TrackNum} - {Title}"
        return ""

    monkeypatch.setattr(fs_mod1.settings_manager, "get", mock_get)
    if fs_mod2:
        monkeypatch.setattr(fs_mod2.settings_manager, "get", mock_get)

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
