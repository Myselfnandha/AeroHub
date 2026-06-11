import logging
from typing import List, Optional
from MovieSongDownloader.providers.jiosaavn_provider import JioSaavnProvider
from MovieSongDownloader.core.models import Album, Track
from MovieSongDownloader.providers.metadata_normalizer import normalize_title
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SoundtrackService")


class SoundtrackService:
    def __init__(self, provider: Optional[JioSaavnProvider] = None):
        self.provider = provider or JioSaavnProvider()

    async def find_soundtracks(
        self,
        movie_title: str,
        movie_year: Optional[int] = None,
        movie_id: Optional[int] = None,
    ) -> List[Album]:
        """Search JioSaavn for soundtrack albums matching the movie, with DB cache support."""
        if movie_id:
            conn = await db.get_connection()
            db_albums = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, movie_id, spotify_id, title, artist, cover_url, "
                        "cover_cached_path, total_tracks, source, source_id FROM albums "
                        "WHERE movie_id = ?"
                    ),
                    (movie_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_albums.append(
                            Album(
                                id=r[0],
                                movie_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                cover_url=r[5],
                                cover_cached_path=r[6],
                                total_tracks=r[7],
                                source=r[8],
                                source_id=r[9],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading albums from DB: {e}")
            finally:
                await conn.close()
            if db_albums:
                logger.info(
                    f"Loaded {len(db_albums)} albums from local database cache for movie ID {movie_id}."
                )
                return db_albums

        if not movie_title:
            return []
        cleaned = normalize_title(movie_title)
        albums = await self.provider.get_soundtrack(cleaned, year=movie_year)
        if not albums and movie_year:
            # Retry without year filter
            albums = await self.provider.get_soundtrack(cleaned, year=None)
        return albums

    async def get_tracks_for_album(
        self, album_id: str, db_album_id: Optional[int] = None
    ) -> List[Track]:
        """Get all tracks for a JioSaavn or Spotify album, with DB cache support."""
        if db_album_id:
            conn = await db.get_connection()
            db_tracks = []
            try:
                async with conn.execute(
                    (
                        "SELECT id, album_id, spotify_id, title, artist, duration_ms, "
                        "track_number, preview_url, source, source_id, download_url "
                        "FROM tracks WHERE album_id = ?"
                    ),
                    (db_album_id,),
                ) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_tracks.append(
                            Track(
                                id=r[0],
                                album_id=r[1],
                                spotify_id=r[2],
                                title=r[3],
                                artist=r[4],
                                duration_ms=r[5],
                                track_number=r[6],
                                preview_url=r[7],
                                source=r[8],
                                source_id=r[9],
                                download_url=r[10],
                            )
                        )
            except Exception as e:
                logger.error(f"Error loading tracks from DB: {e}")
            finally:
                await conn.close()
            if db_tracks:
                logger.info(
                    f"Loaded {len(db_tracks)} tracks from local database cache for album ID {db_album_id}."
                )
                return db_tracks

        if not album_id:
            return []

        # Check album source from DB if db_album_id is provided
        source = "jiosaavn"
        spotify_url = None
        if db_album_id:
            conn = await db.get_connection()
            try:
                async with conn.execute(
                    "SELECT source, source_id FROM albums WHERE id = ?", (db_album_id,)
                ) as c:
                    row = await c.fetchone()
                    if row:
                        source = row[0]
                        if source == "spotify":
                            spotify_url = row[1]
            except Exception as e:
                logger.error(f"Error checking album source: {e}")
            finally:
                await conn.close()

        # Route to SpotifyProvider if source is Spotify
        if source == "spotify" or "spotify.com" in album_id or len(album_id) == 22:
            from MovieSongDownloader.providers.spotify_provider import SpotifyProvider

            spotify_prov = SpotifyProvider()
            url_or_id = spotify_url or album_id
            try:
                _, _, tracks = await spotify_prov.get_spotify_album_or_track(url_or_id)
                return tracks
            except Exception as e:
                logger.error(f"Failed to fetch Spotify tracks for {url_or_id}: {e}")
                return []

        tracks = await self.provider.get_tracks(album_id)
        for t in tracks:
            t.title = normalize_title(t.title)
        return tracks

    async def get_album_details(self, album_id: str) -> Optional[Album]:
        """Get album metadata from JioSaavn."""
        return await self.provider.get_album_details(album_id)

    async def search_songs(self, query: str, limit: int = 10) -> List[Track]:
        """Direct song search on JioSaavn."""
        return await self.provider.search_songs(query, limit=limit)
