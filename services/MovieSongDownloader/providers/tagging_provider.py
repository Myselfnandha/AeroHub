import os
import logging
from typing import Optional
from MovieSongDownloader.providers.base import BaseTaggingProvider
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TYER, TRCK, ID3NoHeaderError
from mutagen.flac import FLAC, Picture

logger = logging.getLogger("MovieSongDownloader.TaggingProvider")


class TaggingProvider(BaseTaggingProvider):
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(image_path, "rb") as f:
            img_data = f.read()
        mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
        ext = file_path.rsplit(".", 1)[-1].lower()

        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("APIC")]:
                audio.tags.pop(k)
            audio.tags.add(
                APIC(encoding=3, mime=mime, type=3, desc="Front Cover", data=img_data)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio.clear_pictures()
            pic = Picture()
            pic.data, pic.type, pic.mime, pic.desc = img_data, 3, mime, "Front Cover"
            audio.add_picture(pic)
            audio.save()

    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        if not os.path.exists(file_path) or not lyrics_content:
            return
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            for k in [k for k in audio.tags.keys() if k.startswith("USLT")]:
                audio.tags.pop(k)
            audio.tags.add(
                USLT(encoding=3, lang="eng", desc="Lyrics", text=lyrics_content)
            )
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["lyrics"] = lyrics_content
            audio["unsyncedlyrics"] = lyrics_content
            audio.save()

    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio not found: {file_path}")
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "mp3":
            audio = self._get_mp3(file_path)
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text=artist))
            audio.tags.add(TALB(encoding=3, text=album))
            audio.tags.add(TRCK(encoding=3, text=str(track_num)))
            if year:
                audio.tags.add(TYER(encoding=3, text=str(year)))
            audio.save()
        elif ext == "flac":
            audio = FLAC(file_path)
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio["tracknumber"] = str(track_num)
            if year:
                audio["date"] = str(year)
            audio.save()

    @staticmethod
    def _get_mp3(path: str) -> MP3:
        try:
            audio = MP3(path, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(path)
            audio.add_tags()
        if audio.tags is None:
            audio.add_tags()
        return audio
