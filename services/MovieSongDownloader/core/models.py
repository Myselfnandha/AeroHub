from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Movie:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source: str = "wikipedia"  # "wikipedia" | "omdb" | "tmdb"
    source_id: str = ""  # Wikipedia page ID or OMDb imdbID
    title: str = ""
    year: Optional[int] = None
    poster_url: Optional[str] = None
    poster_cached_path: Optional[str] = None
    overview: Optional[str] = None
    language: Optional[str] = None
    rating: Optional[str] = None  # IMDb rating from OMDb
    cast_info: Optional[str] = None  # Comma-separated top cast
    release_date: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    ott_providers: List[dict] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Album:
    id: Optional[int] = None
    movie_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn album ID
    title: str = ""
    artist: Optional[str] = None
    cover_url: Optional[str] = None
    cover_cached_path: Optional[str] = None
    total_tracks: Optional[int] = None
    composer: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Track:
    id: Optional[int] = None
    album_id: Optional[int] = None
    spotify_id: Optional[str] = None  # Legacy
    source: str = "jiosaavn"  # "jiosaavn" | "spotify"
    source_id: str = ""  # JioSaavn track ID
    title: str = ""
    artist: Optional[str] = None
    duration_ms: int = 0
    track_number: int = 0
    preview_url: Optional[str] = None
    download_url: Optional[str] = None  # Direct stream URL from JioSaavn
    isrc: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DownloadJob:
    id: Optional[int] = None
    track_id: int = 0
    status: str = "queued"
    progress: float = 0.0
    output_path: Optional[str] = None
    format: str = "mp3"
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Joined metadata for UI display
    track_title: Optional[str] = None
    track_artist: Optional[str] = None
    album_title: Optional[str] = None
    movie_title: Optional[str] = None
    cover_cached_path: Optional[str] = None


@dataclass
class WatchlistItem:
    id: Optional[int] = None
    tmdb_id: int = 0  # Legacy, kept for backward compat
    source_id: str = ""
    title: str = ""
    expected_release: Optional[str] = None
    last_checked: Optional[str] = None
    auto_download: bool = True
    status: str = "watching"
    created_at: Optional[str] = None
