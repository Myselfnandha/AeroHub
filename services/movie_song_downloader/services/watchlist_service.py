import logging
from datetime import datetime
from typing import List
from movie_song_downloader.core.database import db
from movie_song_downloader.core.models import WatchlistItem, Movie, Album, Track
from movie_song_downloader.providers.wikipedia_provider import WikipediaProvider
from movie_song_downloader.services.soundtrack_service import SoundtrackService
from movie_song_downloader.core.job_queue import job_queue

logger = logging.getLogger("movie_song_downloader.WatchlistService")


class WatchlistService:
    def __init__(self, wiki=None, soundtrack=None):
        self.wiki = wiki or WikipediaProvider()
        self.soundtrack = soundtrack or SoundtrackService()

    async def add_to_watchlist(self, movie: Movie, auto_download: bool = True) -> int:
        conn = await db.get_connection()
        try:
            c = await conn.execute(
                (
                    "INSERT INTO watchlist (tmdb_id, source_id, title, expected_release, "
                    "auto_download, status, last_checked) "
                    "VALUES (?, ?, ?, ?, ?, 'watching', datetime('now'))"
                ),
                (
                    movie.tmdb_id,
                    movie.source_id,
                    movie.title,
                    movie.year,
                    1 if auto_download else 0,
                ),
            )
            await conn.commit()
            return c.lastrowid
        finally:
            await conn.close()

    async def get_watchlist(self) -> List[WatchlistItem]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                (
                    "SELECT id, tmdb_id, title, expected_release, last_checked, "
                    "auto_download, status, created_at FROM watchlist"
                )
            ) as c:
                return [
                    WatchlistItem(
                        id=r[0],
                        tmdb_id=r[1],
                        title=r[2],
                        expected_release=r[3],
                        last_checked=r[4],
                        auto_download=bool(r[5]),
                        status=r[6],
                        created_at=r[7],
                    )
                    for r in await c.fetchall()
                ]
        finally:
            await conn.close()

    async def check_releases_and_trigger(self) -> None:
        items = await self.get_watchlist()
        conn = await db.get_connection()
        try:
            for item in items:
                if item.status != "watching":
                    continue
                try:
                    results = await self.wiki.search(item.title)
                    target = next(
                        (m for m in results if m.title.lower() == item.title.lower()),
                        None,
                    )
                    if not target:
                        continue
                    await conn.execute(
                        "UPDATE watchlist SET last_checked=datetime('now') WHERE id=?",
                        (item.id,),
                    )
                    await conn.commit()
                    if target.year and target.year <= datetime.now().year:
                        status = "found"
                        if item.auto_download:
                            albums = await self.soundtrack.find_soundtracks(
                                item.title, movie_year=target.year
                            )
                            if albums:
                                best = albums[0]
                                tracks = await self.soundtrack.get_tracks_for_album(
                                    best.source_id
                                )
                                mid = await self._ensure_movie(conn, target)
                                aid = await self._ensure_album(conn, mid, best)
                                for t in tracks:
                                    tid = await self._ensure_track(conn, aid, t)
                                    await job_queue.enqueue(tid)
                                status = "downloaded"
                        await conn.execute(
                            "UPDATE watchlist SET status=? WHERE id=?",
                            (status, item.id),
                        )
                        await conn.commit()
                except Exception as e:
                    logger.error(f"Watchlist check error for {item.title}: {e}")
        finally:
            await conn.close()

    async def _ensure_movie(self, conn, m: Movie) -> int:
        async with conn.execute(
            "SELECT id FROM movies WHERE source_id=? AND source=?",
            (m.source_id, m.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        # Fallback: check by title+year
        async with conn.execute(
            "SELECT id FROM movies WHERE title=? AND year=?", (m.title, m.year)
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO movies (tmdb_id, source, source_id, title, year, poster_url, "
                "overview, language, rating, cast_info) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                m.tmdb_id,
                m.source,
                m.source_id,
                m.title,
                m.year,
                m.poster_url,
                m.overview,
                m.language,
                m.rating,
                m.cast_info,
            ),
        )
        return c.lastrowid

    async def _ensure_album(self, conn, movie_id: int, a: Album) -> int:
        async with conn.execute(
            "SELECT id FROM albums WHERE source_id=? AND source=?",
            (a.source_id, a.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, artist, "
                "cover_url, total_tracks) VALUES (?,?,?,?,?,?,?,?)"
            ),
            (
                movie_id,
                a.spotify_id,
                a.source,
                a.source_id,
                a.title,
                a.artist,
                a.cover_url,
                a.total_tracks,
            ),
        )
        return c.lastrowid

    async def _ensure_track(self, conn, album_id: int, t: Track) -> int:
        async with conn.execute(
            "SELECT id FROM tracks WHERE source_id=? AND source=?",
            (t.source_id, t.source),
        ) as c:
            r = await c.fetchone()
            if r:
                return r[0]
        c = await conn.execute(
            (
                "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, "
                "duration_ms, track_number, preview_url, download_url) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"
            ),
            (
                album_id,
                t.spotify_id,
                t.source,
                t.source_id,
                t.title,
                t.artist,
                t.duration_ms,
                t.track_number,
                t.preview_url,
                t.download_url,
            ),
        )
        return c.lastrowid
