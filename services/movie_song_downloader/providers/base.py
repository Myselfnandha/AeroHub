from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable
from movie_song_downloader.core.models import Movie, Album, Track


class BaseMovieProvider(ABC):
    @abstractmethod
    async def search(self, query: str, **filters) -> List[Movie]:
        pass

    @abstractmethod
    async def get_today_releases(self, region: str = "IN") -> List[Movie]:
        pass

    @abstractmethod
    async def get_watch_providers(
        self, source_id: str, region: str = "IN"
    ) -> List[dict]:
        pass


class BaseSoundtrackProvider(ABC):
    @abstractmethod
    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        pass


class BaseDownloadProvider(ABC):
    @abstractmethod
    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        pass


class BaseLyricsProvider(ABC):
    @abstractmethod
    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        pass


class BaseTaggingProvider(ABC):
    @abstractmethod
    async def embed_cover(self, file_path: str, image_path: str) -> None:
        pass

    @abstractmethod
    async def embed_lyrics(
        self, file_path: str, lyrics_content: str, is_synced: bool = False
    ) -> None:
        pass

    @abstractmethod
    async def embed_metadata(
        self,
        file_path: str,
        title: str,
        artist: str,
        album: str,
        year: Optional[int] = None,
        track_num: int = 1,
    ) -> None:
        pass
