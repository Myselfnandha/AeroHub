import logging
import json
import asyncio
from typing import List, Optional, Callable, Any
from movie_song_downloader.providers.wikipedia_provider import WikipediaProvider
from movie_song_downloader.providers.omdb_provider import OMDbProvider
from movie_song_downloader.core.models import Movie, Album, Track
from movie_song_downloader.core.database import db

logger = logging.getLogger("movie_song_downloader.MovieService")


class MovieService:
    def __init__(self, wiki_provider=None, omdb_provider=None):
        self.wiki = wiki_provider or WikipediaProvider()
        self.omdb = omdb_provider or OMDbProvider()

    async def _db_get_movies_by_year(self, year: int) -> List[Movie]:
        conn = await db.get_connection()
        movies = []
        try:
            async with conn.execute(
                "SELECT id, tmdb_id, source, source_id, title, year, poster_url, poster_cached_path, "
                "overview, language, genres, ott_providers, rating, cast_info, release_date "
                "FROM movies WHERE year=? ORDER BY release_date DESC, id DESC",
                (year,),
            ) as c:
                rows = await c.fetchall()
                for r in rows:
                    movies.append(
                        Movie(
                            id=r[0],
                            tmdb_id=r[1],
                            source=r[2],
                            source_id=r[3],
                            title=r[4],
                            year=r[5],
                            poster_url=r[6],
                            poster_cached_path=r[7],
                            overview=r[8],
                            language=r[9],
                            genres=json.loads(r[10]) if r[10] else [],
                            ott_providers=json.loads(r[11]) if r[11] else [],
                            rating=r[12],
                            cast_info=r[13],
                            release_date=r[14],
                        )
                    )
        except Exception as e:
            logger.error(f"Error loading movies by year: {e}")
        finally:
            await conn.close()
        return movies

    async def _db_save_movie_album_tracks(
        self, movie: Movie, album: Album, tracks: List[Track]
    ) -> None:
        # Download and cache images to avoid ISP blocking in the Flutter client UI
        from movie_song_downloader.core.cache_manager import image_cache

        if movie.poster_url and not movie.poster_cached_path:
            try:
                movie.poster_cached_path = await image_cache.get_or_download(
                    movie.poster_url, "poster"
                )
            except Exception as ie:
                logger.error(f"Failed to cache movie poster during save: {ie}")

        if album and album.cover_url and not album.cover_cached_path:
            try:
                album.cover_cached_path = await image_cache.get_or_download(
                    album.cover_url, "cover"
                )
            except Exception as ie:
                logger.error(f"Failed to cache album cover during save: {ie}")

        conn = await db.get_connection()
        try:
            # 1. Insert Movie
            async with conn.execute(
                "SELECT id FROM movies WHERE source_id=? AND source=?",
                (movie.source_id, movie.source),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    movie_id = row[0]
                    # Update fields in case it was a stub previously
                    await conn.execute(
                        "UPDATE movies SET poster_url=?, poster_cached_path=?, rating=?, cast_info=?, "
                        "overview=?, genres=?, ott_providers=?, release_date=? WHERE id=?",
                        (
                            movie.poster_url,
                            movie.poster_cached_path,
                            movie.rating,
                            movie.cast_info,
                            movie.overview,
                            json.dumps(movie.genres),
                            json.dumps(movie.ott_providers),
                            movie.release_date,
                            movie_id,
                        ),
                    )
                else:
                    tmdb_id = movie.tmdb_id
                    if tmdb_id == 0 or tmdb_id is None:
                        import hashlib

                        hash_input = f"{movie.title}|{movie.source_id or ''}"
                        tmdb_id = int(
                            hashlib.md5(hash_input.encode("utf-8")).hexdigest()[:8], 16
                        )

                    genres_json = json.dumps(movie.genres)
                    ott_json = json.dumps(movie.ott_providers)
                    m_cursor = await conn.execute(
                        (
                            "INSERT INTO movies (tmdb_id, source, source_id, title, year, poster_url, "
                            "poster_cached_path, overview, language, genres, ott_providers, rating, "
                            "cast_info, release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        ),
                        (
                            tmdb_id,
                            movie.source,
                            movie.source_id,
                            movie.title,
                            movie.year,
                            movie.poster_url,
                            movie.poster_cached_path,
                            movie.overview,
                            movie.language,
                            genres_json,
                            ott_json,
                            movie.rating,
                            movie.cast_info,
                            movie.release_date,
                        ),
                    )
                    movie_id = m_cursor.lastrowid

            # 2. Insert Album (if resolved)
            if album:
                async with conn.execute(
                    "SELECT id FROM albums WHERE source_id=? AND source=?",
                    (album.source_id, album.source),
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        album_id = row[0]
                        # Update cover cached path and composer if it was updated
                        await conn.execute(
                            "UPDATE albums SET cover_cached_path = ?, composer = ? WHERE id = ?",
                            (album.cover_cached_path, album.composer, album_id),
                        )
                    else:
                        a_cursor = await conn.execute(
                            (
                                "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, "
                                "artist, cover_url, cover_cached_path, total_tracks, composer) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                            ),
                            (
                                movie_id,
                                album.spotify_id,
                                album.source,
                                album.source_id,
                                album.title,
                                album.artist,
                                album.cover_url,
                                album.cover_cached_path,
                                album.total_tracks,
                                album.composer,
                            ),
                        )
                        album_id = a_cursor.lastrowid

                # 3. Insert Tracks
                if tracks:
                    for track in tracks:
                        async with conn.execute(
                            "SELECT id FROM tracks WHERE source_id=? AND source=?",
                            (track.source_id, track.source),
                        ) as cursor:
                            row = await cursor.fetchone()
                            if not row:
                                await conn.execute(
                                    (
                                        "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, "
                                        "duration_ms, track_number, preview_url, download_url, isrc) "
                                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                                    ),
                                    (
                                        album_id,
                                        track.spotify_id,
                                        track.source,
                                        track.source_id,
                                        track.title,
                                        track.artist,
                                        track.duration_ms,
                                        track.track_number,
                                        track.preview_url,
                                        track.download_url,
                                        track.isrc,
                                    ),
                                )
            await conn.commit()
        except Exception as e:
            logger.error(f"Error saving movie-album-tracks cache: {e}")
        finally:
            await conn.close()

    async def search_movies(
        self,
        query: str,
        year: Optional[int] = None,
        on_progress: Optional[Callable[[float], None]] = None,
    ) -> List[Movie]:
        """Search movies: check Wikipedia first, then enrich and check DB. Fallback to DB search if offline."""
        if not query:
            if on_progress:
                on_progress(100.0)
            return []

        if on_progress:
            on_progress(10.0)
        logger.info(f"Searching Wikipedia for '{query}'...")
        movies = await self.wiki.search(query, year=year)

        # If Wikipedia returned nothing, fallback to local DB search
        if not movies:
            logger.info(
                "Wikipedia search returned no results. Falling back to local database search..."
            )
            if on_progress:
                on_progress(50.0)
            conn = await db.get_connection()
            db_results = []
            try:
                sql = (
                    "SELECT id, tmdb_id, source, source_id, title, year, poster_url, poster_cached_path, "
                    "overview, language, genres, ott_providers, rating, cast_info, release_date "
                    "FROM movies WHERE title LIKE ?"
                )
                params = [f"%{query}%"]
                if year:
                    sql += " AND year = ?"
                    params.append(year)
                async with conn.execute(sql, params) as c:
                    rows = await c.fetchall()
                    for r in rows:
                        db_results.append(
                            Movie(
                                id=r[0],
                                tmdb_id=r[1],
                                source=r[2],
                                source_id=r[3],
                                title=r[4],
                                year=r[5],
                                poster_url=r[6],
                                poster_cached_path=r[7],
                                overview=r[8],
                                language=r[9],
                                genres=json.loads(r[10]) if r[10] else [],
                                ott_providers=json.loads(r[11]) if r[11] else [],
                                rating=r[12],
                                cast_info=r[13],
                                release_date=r[14],
                            )
                        )
            except Exception as e:
                logger.error(f"Local database search failed: {e}")
            finally:
                await conn.close()
            if on_progress:
                on_progress(100.0)
            return db_results

        if on_progress:
            on_progress(20.0)

        from movie_song_downloader.services.soundtrack_service import SoundtrackService

        soundtrack_service = SoundtrackService()

        # Enrich and cache the top 5 results to keep search fast
        enriched = []
        movies_to_enrich = movies[:5]
        total_to_enrich = len(movies_to_enrich) if movies_to_enrich else 1
        completed_count = 0

        for movie in movies_to_enrich:
            try:
                conn = await db.get_connection()
                db_movie = None
                try:
                    async with conn.execute(
                        "SELECT id FROM movies WHERE source_id=? AND source=?",
                        (movie.source_id, movie.source),
                    ) as cursor:
                        row = await cursor.fetchone()
                        if row:
                            async with conn.execute(
                                (
                                    "SELECT id, tmdb_id, source, source_id, title, year, poster_url, "
                                    "poster_cached_path, overview, language, genres, ott_providers, rating, "
                                    "cast_info, release_date FROM movies WHERE id=?"
                                ),
                                (row[0],),
                            ) as c2:
                                r = await c2.fetchone()
                                db_movie = Movie(
                                    id=r[0],
                                    tmdb_id=r[1],
                                    source=r[2],
                                    source_id=r[3],
                                    title=r[4],
                                    year=r[5],
                                    poster_url=r[6],
                                    poster_cached_path=r[7],
                                    overview=r[8],
                                    language=r[9],
                                    genres=json.loads(r[10]) if r[10] else [],
                                    ott_providers=json.loads(r[11]) if r[11] else [],
                                    rating=r[12],
                                    cast_info=r[13],
                                    release_date=r[14],
                                )
                finally:
                    await conn.close()

                # If movie exists in DB, check if it's a stub (i.e. lacks ratings, poster, or albums)
                needs_enrichment = True
                if db_movie:
                    conn = await db.get_connection()
                    has_album = False
                    try:
                        async with conn.execute(
                            "SELECT id FROM albums WHERE movie_id = ?", (db_movie.id,)
                        ) as c:
                            if await c.fetchone():
                                has_album = True
                    finally:
                        await conn.close()

                    if db_movie.rating and db_movie.poster_url and has_album:
                        needs_enrichment = False
                        movie = db_movie

                if needs_enrichment:
                    logger.info(
                        f"Enriching movie details (before/after DB check) for {movie.title}..."
                    )
                    movie = await self.omdb.enrich_movie(movie)

                    # Fallback to Wikipedia details if OMDb failed or key is invalid
                    if (
                        (not movie.poster_url or not movie.overview)
                        and movie.source == "wikipedia"
                        and movie.source_id
                    ):
                        try:
                            wiki_details = await self.wiki.get_movie_details(
                                movie.source_id
                            )
                            if wiki_details:
                                if not movie.poster_url and wiki_details.poster_url:
                                    movie.poster_url = wiki_details.poster_url
                                if not movie.overview and wiki_details.overview:
                                    movie.overview = wiki_details.overview
                        except Exception as we:
                            logger.error(
                                f"Wikipedia details fallback failed for {movie.title}: {we}"
                            )

                    movie.ott_providers = (
                        await self.wiki.get_watch_providers(movie.source_id)
                        if movie.source_id
                        else []
                    )

                    # Download and cache poster
                    if movie.poster_url:
                        from movie_song_downloader.core.cache_manager import image_cache

                        movie.poster_cached_path = await image_cache.get_or_download(
                            movie.poster_url, "poster"
                        )

                    from movie_song_downloader.providers.metadata_normalizer import (
                        normalize_title,
                    )

                    clean_title = normalize_title(movie.title)
                    albums = await soundtrack_service.find_soundtracks(
                        clean_title, movie.year
                    )
                    best_album = None
                    tracks = []
                    if albums:
                        best_album = albums[0]
                        # Cache album cover
                        if best_album.cover_url:
                            from movie_song_downloader.core.cache_manager import (
                                image_cache,
                            )

                            best_album.cover_cached_path = (
                                await image_cache.get_or_download(
                                    best_album.cover_url, "cover"
                                )
                            )
                        tracks = await soundtrack_service.get_tracks_for_album(
                            best_album.source_id
                        )

                        # Enrich with MusicBrainz
                        try:
                            from movie_song_downloader.providers.musicbrainz_provider import (
                                MusicBrainzProvider,
                            )

                            mb_provider = MusicBrainzProvider()
                            mb_composer, mb_isrcs = await mb_provider.enrich_album(
                                best_album, tracks
                            )
                            if mb_composer:
                                best_album.composer = mb_composer
                            for t in tracks:
                                if t.title in mb_isrcs:
                                    t.isrc = mb_isrcs[t.title]
                        except Exception as mbe:
                            logger.error(
                                f"MusicBrainz enrichment failed for {movie.title}: {mbe}"
                            )

                    await self._db_save_movie_album_tracks(movie, best_album, tracks)

                    # Reload from DB to ensure we return the record with correct local IDs
                    conn = await db.get_connection()
                    try:
                        async with conn.execute(
                            (
                                "SELECT id, tmdb_id, source, source_id, title, year, poster_url, "
                                "poster_cached_path, overview, language, genres, ott_providers, rating, "
                                "cast_info, release_date FROM movies WHERE source_id=? AND source=?"
                            ),
                            (movie.source_id, movie.source),
                        ) as c:
                            r = await c.fetchone()
                            if r:
                                movie = Movie(
                                    id=r[0],
                                    tmdb_id=r[1],
                                    source=r[2],
                                    source_id=r[3],
                                    title=r[4],
                                    year=r[5],
                                    poster_url=r[6],
                                    poster_cached_path=r[7],
                                    overview=r[8],
                                    language=r[9],
                                    genres=json.loads(r[10]) if r[10] else [],
                                    ott_providers=json.loads(r[11]) if r[11] else [],
                                    rating=r[12],
                                    cast_info=r[13],
                                    release_date=r[14],
                                )
                    finally:
                        await conn.close()

            except Exception as e:
                logger.error(f"Search enrichment/caching failed for {movie.title}: {e}")
            finally:
                completed_count += 1
                if on_progress:
                    pct = 20.0 + (completed_count / total_to_enrich) * 75.0
                    on_progress(min(pct, 99.0))
            enriched.append(movie)

        for movie in movies[5:]:
            enriched.append(movie)

        if on_progress:
            if asyncio.iscoroutinefunction(on_progress):
                await on_progress(100.0, "Finished fetching updates")
            else:
                on_progress(100.0, "Finished fetching updates")
        return enriched

    async def get_cached_releases(self) -> List[Movie]:
        """Get recent Tamil releases only from the local database cache."""
        import datetime
        current_year = datetime.date.today().year
        cached_movies = await self._db_get_movies_by_year(current_year)
        if cached_movies:
            logger.info(f"Loaded {len(cached_movies)} current year releases from local database cache.")
            return cached_movies
        return []

    async def get_today_releases(
        self, region: str = "IN", on_progress: Optional[Callable[[float, str], Any]] = None
    ) -> List[Movie]:
        """Get recent Tamil releases from Wikipedia, enriched with OMDb and cached in DB in parallel."""
        import datetime

        current_date_str = datetime.date.today().isoformat()
        current_year = datetime.date.today().year

        from movie_song_downloader.core.settings_manager import settings_manager

        last_fetch_date = await settings_manager.get("last_fetch_date")

        cached_movies = await self._db_get_movies_by_year(current_year)
        if cached_movies and last_fetch_date == current_date_str:
            logger.info(
                "Loaded %s current year releases from local database cache. "
                "Last fetch date matches today (%s).",
                len(cached_movies),
                current_date_str,
            )
            if on_progress:
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(100.0, "Up to date")
                else:
                    on_progress(100.0, "Up to date")
            return cached_movies


        if on_progress:
            if asyncio.iscoroutinefunction(on_progress):
                await on_progress(10.0, "Scraping Wikipedia releases...")
            else:
                on_progress(10.0, "Scraping Wikipedia releases...")
        scraping_limit = int(await settings_manager.get("scraping_limit") or 5)

        logger.info(
            "Local database cache is outdated or empty (Last fetch: %s, Today: %s). "
            "Scraping Wikipedia releases...",
            last_fetch_date,
            current_date_str,
        )
        try:
            movies = await self.wiki.get_today_releases(region=region)
            if not movies:
                logger.warning(
                    "Wikipedia returned no movies. Falling back to cached movies if available."
                )
                if cached_movies:
                    if on_progress:
                        on_progress(100.0)
                    return cached_movies
                movies = []
        except Exception as e:
            logger.error(
                "Error scraping Wikipedia releases: %s. Falling back to cached movies if available.",
                e,
            )
            if cached_movies:
                if on_progress:
                    on_progress(100.0)
                return cached_movies
            raise

        if on_progress:
            if asyncio.iscoroutinefunction(on_progress):
                await on_progress(20.0, "Enriching movie metadata...")
            else:
                on_progress(20.0, "Enriching movie metadata...")

        from movie_song_downloader.services.soundtrack_service import SoundtrackService

        soundtrack_service = SoundtrackService()

        # Database save lock to prevent sqlite database locked errors
        db_save_lock = asyncio.Lock()

        completed_count = 0
        total_movies = len(movies) if movies else 1

        async def enrich_single_movie(movie, idx):
            nonlocal completed_count
            try:
                # Enrich and cache only within the fetching limit to save bandwidth
                if idx < scraping_limit:
                    movie = await self.omdb.enrich_movie(movie)

                    # Fallback to Wikipedia details if OMDb failed or key is invalid
                    if (
                        (not movie.poster_url or not movie.overview)
                        and movie.source == "wikipedia"
                        and movie.source_id
                    ):
                        try:
                            wiki_details = await self.wiki.get_movie_details(
                                movie.source_id
                            )
                            if wiki_details:
                                if not movie.poster_url and wiki_details.poster_url:
                                    movie.poster_url = wiki_details.poster_url
                                if not movie.overview and wiki_details.overview:
                                    movie.overview = wiki_details.overview
                        except Exception as we:
                            logger.error(
                                f"Wikipedia details fallback failed for {movie.title}: {we}"
                            )

                    movie.ott_providers = (
                        await self.wiki.get_watch_providers(
                            movie.source_id, region=region
                        )
                        if movie.source_id
                        else []
                    )

                    # Download and cache the poster!
                    if movie.poster_url:
                        from movie_song_downloader.core.cache_manager import image_cache

                        movie.poster_cached_path = await image_cache.get_or_download(
                            movie.poster_url, "poster"
                        )

                    from movie_song_downloader.providers.metadata_normalizer import (
                        normalize_title,
                    )

                    clean_title = normalize_title(movie.title)

                    albums = await soundtrack_service.find_soundtracks(
                        clean_title, movie.year
                    )
                    best_album = None
                    tracks = []
                    if albums:
                        best_album = albums[0]
                        # Cache cover art
                        if best_album.cover_url:
                            from movie_song_downloader.core.cache_manager import (
                                image_cache,
                            )

                            best_album.cover_cached_path = (
                                await image_cache.get_or_download(
                                    best_album.cover_url, "cover"
                                )
                            )
                        tracks = await soundtrack_service.get_tracks_for_album(
                            best_album.source_id
                        )

                        # MusicBrainz enrichment
                        try:
                            from movie_song_downloader.providers.musicbrainz_provider import (
                                MusicBrainzProvider,
                            )

                            mb_provider = MusicBrainzProvider()
                            mb_composer, mb_isrcs = await mb_provider.enrich_album(
                                best_album, tracks
                            )
                            if mb_composer:
                                best_album.composer = mb_composer
                            for t in tracks:
                                if t.title in mb_isrcs:
                                    t.isrc = mb_isrcs[t.title]
                        except Exception as mbe:
                            logger.error(
                                f"MusicBrainz enrichment failed for {movie.title}: {mbe}"
                            )

                    async with db_save_lock:
                        await self._db_save_movie_album_tracks(
                            movie, best_album, tracks
                        )
                else:
                    # Save as a stub entry to the database, but still download and cache the poster immediately
                    if movie.poster_url:
                        try:
                            from movie_song_downloader.core.cache_manager import (
                                image_cache,
                            )

                            movie.poster_cached_path = (
                                await image_cache.get_or_download(
                                    movie.poster_url, "poster"
                                )
                            )
                        except Exception as ce:
                            logger.error(f"Failed to cache stub poster: {ce}")
                    async with db_save_lock:
                        await self._db_save_movie_album_tracks(movie, None, [])

            except Exception as e:
                logger.error(
                    f"Parallel enrich/cache failed for {movie.title}: {e}",
                    exc_info=True,
                )
            finally:
                completed_count += 1
                if on_progress:
                    pct = 20.0 + (completed_count / total_movies) * 80.0
                    msg = f"Processed {completed_count}/{total_movies}: {movie.title}"
                    if asyncio.iscoroutinefunction(on_progress):
                        await on_progress(pct, msg)
                    else:
                        on_progress(pct, msg)

        # Process movies in parallel batches of 10
        batch_size = 10
        if movies:
            for i in range(0, len(movies), batch_size):
                batch = movies[i:i+batch_size]
                tasks = [
                    enrich_single_movie(movie, i + idx)
                    for idx, movie in enumerate(batch)
                ]
                await asyncio.gather(*tasks)

            # Successfully fetched and cached. Save the current date.
            try:
                await settings_manager.set("last_fetch_date", current_date_str)
                logger.info(f"Saved last fetch date setting as {current_date_str}.")
            except Exception as se:
                logger.error(f"Failed to save last_fetch_date: {se}")

        db_movies = await self._db_get_movies_by_year(current_year)
        if on_progress:
            on_progress(100.0)
        if db_movies:
            return db_movies
        return movies
