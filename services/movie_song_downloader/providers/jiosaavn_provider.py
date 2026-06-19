import logging
import hashlib
from typing import List, Optional
from jiosaavnpy import JioSaavn

from movie_song_downloader.providers.base import BaseSoundtrackProvider
from movie_song_downloader.core.models import Album, Track
from movie_song_downloader.core.rate_limiter import rate_limiter, providers_logger
from movie_song_downloader.core.cache_manager import api_cache

logger = logging.getLogger("movie_song_downloader.JioSaavnProvider")


class JioSaavnProvider(BaseSoundtrackProvider):
    def __init__(self):
        self._client = JioSaavn()

    async def get_soundtrack(
        self, movie_title: str, year: Optional[int] = None
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching movie title."""
        query = movie_title
        if year:
            query = f"{movie_title} {year}"

        cache_key = f"jiosaavn:album_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_albums(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_albums(query, limit=8)
            if not results:
                return []

            albums = []
            for item in results:
                cover = None
                thumbs = item.get("thumbnails", {}).get("quality", {})
                cover = (
                    thumbs.get("500x500")
                    or thumbs.get("150x150")
                    or thumbs.get("50x50")
                )

                album = Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    spotify_id=None,
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
                albums.append(album)

            # Cache raw results
            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=search_albums results={len(albums)}"
            )
            return albums

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=search_albums'
            )
            logger.error(f"JioSaavn album search failed: {e}")
            return []

    async def get_tracks(self, album_id: str) -> List[Track]:
        """Fetch all tracks for a JioSaavn album."""
        cache_key = f"jiosaavn:album_tracks:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info or "tracks" not in info:
                return []

            raw_tracks = info["tracks"]
            tracks = []
            for idx, item in enumerate(raw_tracks, start=1):
                # Get best quality stream URL
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                    or streams.get("low_quality")
                )

                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        spotify_id=None,
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", raw_tracks, ttl=86400)
            providers_logger.info(
                f"provider=jiosaavn success=True endpoint=album_info tracks={len(tracks)}"
            )
            return tracks

        except Exception as e:
            providers_logger.error(
                f'provider=jiosaavn success=False error="{e}" endpoint=album_info'
            )
            logger.error(f"JioSaavn album tracks failed: {e}")
            return []

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Fetch album metadata from JioSaavn."""
        cache_key = f"jiosaavn:album_detail:{album_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None and isinstance(cached, dict):
            return self._dict_to_album(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            info = self._client.album_info(album_id)
            if not info:
                return None

            cover = None
            thumbs = info.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")

            album = Album(
                source="jiosaavn",
                source_id=info.get("album_id", album_id),
                title=info.get("title", ""),
                artist=info.get("primary_artists", "Unknown"),
                cover_url=cover,
                total_tracks=len(info.get("tracks", [])),
            )

            await api_cache.set(
                cache_key,
                "jiosaavn",
                {
                    "album_id": album.source_id,
                    "title": album.title,
                    "artist": album.artist,
                    "cover_url": album.cover_url,
                    "total_tracks": album.total_tracks,
                },
                ttl=86400,
            )

            return album

        except Exception as e:
            logger.error(f"JioSaavn album details failed: {e}")
            return None

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        cache_key = f"jiosaavn:song_search:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return self._parse_cached_tracks(cached)

        await rate_limiter.acquire("jiosaavn")
        try:
            results = self._client.search_songs(query, limit=limit)
            if not results:
                return []

            tracks = []
            for idx, item in enumerate(results, start=1):
                streams = item.get("stream_urls", {})
                best_url = (
                    streams.get("very_high_quality")
                    or streams.get("high_quality")
                    or streams.get("medium_quality")
                )
                duration_sec = int(item.get("duration", 0))

                tracks.append(
                    Track(
                        source="jiosaavn",
                        source_id=item.get("track_id", ""),
                        title=item.get("title", ""),
                        artist=item.get("primary_artists", "Unknown"),
                        duration_ms=duration_sec * 1000,
                        track_number=idx,
                        preview_url=streams.get("low_quality"),
                        download_url=best_url,
                    )
                )

            await api_cache.set(cache_key, "jiosaavn", results, ttl=86400)
            return tracks

        except Exception as e:
            logger.error(f"JioSaavn song search failed: {e}")
            return []

    def _parse_cached_albums(self, cached_data: list) -> List[Album]:
        """Convert cached raw JioSaavn album dicts back to Album objects."""
        albums = []
        for item in cached_data:
            cover = None
            thumbs = item.get("thumbnails", {}).get("quality", {})
            cover = thumbs.get("500x500") or thumbs.get("150x150")
            albums.append(
                Album(
                    source="jiosaavn",
                    source_id=item.get("album_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("artists", "Unknown"),
                    cover_url=cover,
                    total_tracks=int(item.get("track_count", 0)),
                )
            )
        return albums

    def _parse_cached_tracks(self, cached_data: list) -> List[Track]:
        """Convert cached raw JioSaavn track dicts back to Track objects."""
        tracks = []
        for idx, item in enumerate(cached_data, start=1):
            streams = item.get("stream_urls", {})
            best_url = (
                streams.get("very_high_quality")
                or streams.get("high_quality")
                or streams.get("medium_quality")
            )
            duration_sec = int(item.get("duration", 0))
            tracks.append(
                Track(
                    source="jiosaavn",
                    source_id=item.get("track_id", ""),
                    title=item.get("title", ""),
                    artist=item.get("primary_artists", "Unknown"),
                    duration_ms=duration_sec * 1000,
                    track_number=idx,
                    preview_url=streams.get("low_quality"),
                    download_url=best_url,
                )
            )
        return tracks

    @staticmethod
    def _dict_to_album(d: dict) -> Album:
        return Album(
            source="jiosaavn",
            source_id=d.get("album_id", ""),
            title=d.get("title", ""),
            artist=d.get("artist", "Unknown"),
            cover_url=d.get("cover_url"),
            total_tracks=d.get("total_tracks", 0),
        )
