import os
import re
import json
import logging
from datetime import datetime
from typing import Tuple
from pathlib import Path
from movie_song_downloader.core.models import Movie, Album, Track
from movie_song_downloader.core.settings_manager import settings_manager

logger = logging.getLogger("movie_song_downloader.FolderService")


class FolderService:
    @staticmethod
    def sanitize_name(name: str) -> str:
        if not name:
            return "Unknown"
        s = re.sub(r'[\\/:*?"<>|]', "-", name)
        return re.sub(r"\s+", " ", s).strip() or "Unknown"

    async def get_target_path(
        self, movie: Movie, album: Album, track: Track, fmt: str = "mp3"
    ) -> Tuple[str, str]:
        output_dir = await settings_manager.get("output_dir")
        folder_tpl = await settings_manager.get("folder_format")
        file_tpl = await settings_manager.get("filename_format")

        tokens = {
            "{Year}": str(movie.year) if movie.year else "Unknown",
            "{Movie}": self.sanitize_name(movie.title),
            "{Artist}": self.sanitize_name(track.artist),
            "{Album}": self.sanitize_name(album.title),
            "{TrackNum}": f"{track.track_number:02d}",
            "{Title}": self.sanitize_name(track.title),
        }

        resolved_folder = folder_tpl
        resolved_file = file_tpl
        for k, v in tokens.items():
            resolved_folder = resolved_folder.replace(k, v)
            resolved_file = resolved_file.replace(k, v)

        parts = [self.sanitize_name(p) for p in resolved_folder.split("/") if p.strip()]
        target_dir = Path(output_dir) / Path(*parts)
        filename = f"{self.sanitize_name(resolved_file)}.{fmt.lower()}"
        return str(target_dir), str(target_dir / filename)

    async def write_movie_metadata(self, movie: Movie, target_dir: str) -> None:
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, "movie.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "tmdb_id": movie.tmdb_id,
                        "title": movie.title,
                        "year": movie.year,
                        "overview": movie.overview,
                        "language": movie.language,
                        "genres": movie.genres,
                        "ott_providers": movie.ott_providers,
                        "exported_at": datetime.now().isoformat(),
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            logger.error(f"movie.json write failed: {e}")

    async def generate_m3u_playlist(self, target_dir: str, album_title: str) -> None:
        if not os.path.exists(target_dir):
            return
        files = sorted(
            f for f in os.listdir(target_dir) if f.lower().endswith((".mp3", ".flac"))
        )
        if not files:
            return
        try:
            with open(
                os.path.join(target_dir, "playlist.m3u"), "w", encoding="utf-8"
            ) as f:
                f.write(f"#EXTM3U\n#PLAYLIST:{album_title}\n\n")
                for name in files:
                    f.write(f"{name}\n")
        except Exception as e:
            logger.error(f"playlist.m3u failed: {e}")
