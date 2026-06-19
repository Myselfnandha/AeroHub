# ruff: noqa: E402
import os
import sys
import importlib
from importlib.abc import MetaPathFinder

# Add workspace root and services directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
services_dir = os.path.join(workspace_root, "services")

if workspace_root not in sys.path:
    sys.path.append(workspace_root)
if services_dir not in sys.path:
    sys.path.append(services_dir)

# Register Redirector so MovieSongDownloader -> movie_song_downloader works seamlessly
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

# Only insert if not already present
if not any(isinstance(finder, MovieSongDownloaderRedirector) for finder in sys.meta_path):
    sys.meta_path.insert(0, MovieSongDownloaderRedirector())

import pytest
import movie_song_downloader.config
from movie_song_downloader.core.database import db


@pytest.fixture(scope="session", autouse=True)
def use_test_database(tmp_path_factory):
    # Redirect DATABASE_PATH to a temporary test database file
    test_db_dir = tmp_path_factory.mktemp("test_db_dir")
    test_db_path = test_db_dir / "test_db.sqlite3"

    # Patch the configuration path and the instantiated database manager path
    movie_song_downloader.config.DATABASE_PATH = test_db_path
    db.db_path = test_db_path

    yield

    # Cleanup after the test session finishes
    if test_db_path.exists():
        try:
            os.remove(test_db_path)
        except Exception:
            pass
