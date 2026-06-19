# movie_song_downloader/ui/state.py

import reflex as rx
import asyncio
import os
import json
import logging
from pathlib import Path
from dataclasses import asdict

from movie_song_downloader.core.database import db
from movie_song_downloader.core.models import Movie, Track
from movie_song_downloader.services.movie_service import MovieService
from movie_song_downloader.services.soundtrack_service import SoundtrackService
from movie_song_downloader.services.watchlist_service import WatchlistService
from movie_song_downloader.services.download_service import download_service
from movie_song_downloader.core.settings_manager import settings_manager
from movie_song_downloader.core.job_queue import job_queue

logger = logging.getLogger("movie_song_downloader.State")


def to_dict(obj):
    if not obj:
        return {}
    return asdict(obj)


class AppState(rx.State):
    # --- Navigation ---
    active_tab: str = "home"

    # Background fetching
    is_fetching_updates: bool = False
    has_new_updates: bool = False
    fetching_status: str = ""
    new_recent_releases: list[dict] = []

    # Subview control for displaying tracks of an album
    selected_movie: dict = {}
    selected_album: dict = {}
    show_songs_view: bool = False

    # --- Home View ---
    recent_releases: list[dict] = []
    watchlist_items: list[dict] = []
    releases_loading: bool = False
    watchlist_loading: bool = False

    # --- Watchlist View ---
    watchlist_btn_text: str = "Check Watchlist"
    watchlist_btn_disabled: bool = False

    # --- Search View ---
    search_query: str = ""
    search_year: str = ""
    search_results: list[dict] = []
    search_loading: bool = False
    search_error: str = ""

    # --- Songs View ---
    album_tracks: list[dict] = []
    tracks_loading: bool = False
    selected_track_ids: list[int] = []  # Checked track database IDs
    select_all: bool = True
    audio_preview_url: str = ""
    download_btn_text: str = "Download Selected"
    download_btn_disabled: bool = False

    # Missing Directory Dialog Control
    missing_dir_dialog_open: bool = False
    pending_download_track_ids: list[int] = []

    # --- Directory Explorer ---
    dir_explorer_open: bool = False
    dir_explorer_path: str = ""
    dir_explorer_items: list[str] = []
    dir_explorer_error: str = ""
    dir_target_setting: str = "output_dir"  # "output_dir" or other settings fields

    # --- Downloads View ---
    download_jobs: list[dict] = []
    downloads_loading: bool = False

    # --- Settings View ---
    omdb_api_key: str = ""
    deezer_arl: str = ""
    output_dir: str = ""
    folder_format: str = ""
    folder_format_dropdown: str = ""
    folder_format_custom: str = ""
    filename_format: str = ""
    filename_format_dropdown: str = ""
    filename_format_custom: str = ""
    audio_format: str = ""
    bitrate: str = ""
    save_lrc_file: bool = True
    embed_lyrics: bool = True
    auto_download: bool = True
    download_provider: str = "spotiflac"
    settings_status_msg: str = ""
    settings_status_color: str = ""

    # --- First-run Setup Wizard ---
    setup_wizard_open: bool = False
    setup_omdb_key: str = ""
    setup_deezer_arl: str = ""
    setup_status_msg: str = ""

    # --- Initialization ---
    async def on_load(self):
        """Runs automatically when page loads."""
        await self.load_settings()
        await self._check_first_run()
        try:
            await download_service.start()
        except Exception as e:
            logger.error(f"Failed to start download worker on page load: {e}")

    # --- Tab Switcher ---
    async def set_tab(self, tab: str):
        self.active_tab = tab
        self.show_songs_view = False
        self.audio_preview_url = ""
        self.settings_status_msg = ""
        yield
        if tab == "home":
            yield AppState.load_home_data
        elif tab == "watchlist":
            yield AppState.load_watchlist_data
        elif tab == "downloads":
            yield AppState.load_download_jobs
        elif tab == "settings":
            yield AppState.load_settings

    # --- Home View Event Handlers ---
    @rx.event(background=True)
    async def load_home_data(self):
        async with self:
            self.releases_loading = True
            self.watchlist_loading = True
        yield

        # 1. Load CACHED releases first for instant display
        try:
            movie_svc = MovieService()
            cached_movies = await movie_svc.get_cached_releases()
            async with self:
                self.recent_releases = [to_dict(m) for m in cached_movies]
        except Exception as e:
            logger.error(f"Error loading home cached releases: {e}")
            async with self:
                self.recent_releases = []
                
        async with self:
            self.releases_loading = False
        yield

        # 2. Trigger background fetch for new releases
        yield AppState.bg_fetch_updates

        # Load watchlist
        await self._reload_watchlist()
        async with self:
            self.watchlist_loading = False

    @rx.event(background=True)
    async def bg_fetch_updates(self):
        async with self:
            self.is_fetching_updates = True
            self.has_new_updates = False
            self.new_recent_releases = []
            self.fetching_status = "Checking for updates..."
        yield

        async def progress_cb(pct: float, status_msg: str = ""):
            async with self:
                if status_msg:
                    self.fetching_status = status_msg
            # Yield not needed natively; background task state changes sync automatically.

        try:
            movie_svc = MovieService()
            new_movies = await movie_svc.get_today_releases("IN", on_progress=progress_cb)
            if new_movies:
                new_releases_dict = [to_dict(m) for m in new_movies]
                if new_releases_dict != self.recent_releases:
                    async with self:
                        self.new_recent_releases = new_releases_dict
                        self.has_new_updates = True
        except Exception as e:
            logger.error(f"Error fetching new updates: {e}")
            
        async with self:
            self.is_fetching_updates = False

    def apply_dashboard_updates(self):
        if self.new_recent_releases:
            self.recent_releases = self.new_recent_releases
        self.has_new_updates = False
        self.new_recent_releases = []

    async def _reload_watchlist(self):
        try:
            watchlist_svc = WatchlistService()
            items = await watchlist_svc.get_watchlist()
            serialized = []
            for i in items:
                d = to_dict(i)
                d["status"] = d["status"].upper()
                serialized.append(d)
            async with self:
                self.watchlist_items = serialized
        except Exception as e:
            logger.error(f"Error reloading watchlist: {e}")
            async with self:
                self.watchlist_items = []

    async def load_watchlist_data(self):
        async with self:
            self.watchlist_loading = True
        yield
        await self._reload_watchlist()
        async with self:
            self.watchlist_loading = False

    async def trigger_watchlist_check(self):
        async with self:
            self.watchlist_btn_text = "Checking..."
            self.watchlist_btn_disabled = True
        yield
        try:
            watchlist_svc = WatchlistService()
            await watchlist_svc.check_releases_and_trigger()
            await self._reload_watchlist()
        except Exception as e:
            logger.error(f"Watchlist check failed: {e}")
        async with self:
            self.watchlist_btn_text = "Check Watchlist"
            self.watchlist_btn_disabled = False

    async def remove_watchlist_item(self, item_id: int):
        conn = await db.get_connection()
        try:
            await conn.execute("DELETE FROM watchlist WHERE id = ?", (item_id,))
            await conn.commit()
            await self._reload_watchlist()
        finally:
            await conn.close()

    async def add_to_watchlist_from_card(self, movie_dict: dict):
        try:
            watchlist_svc = WatchlistService()
            # Reconstruct Movie object
            genres_val = movie_dict.get("genres", [])
            if isinstance(genres_val, str):
                genres_val = json.loads(genres_val)
            ott_val = movie_dict.get("ott_providers", [])
            if isinstance(ott_val, str):
                ott_val = json.loads(ott_val)

            movie = Movie(
                id=movie_dict.get("id"),
                source=movie_dict.get("source", "wikipedia"),
                source_id=movie_dict.get("source_id", ""),
                title=movie_dict.get("title", ""),
                year=movie_dict.get("year"),
                poster_url=movie_dict.get("poster_url"),
                poster_cached_path=movie_dict.get("poster_cached_path"),
                overview=movie_dict.get("overview"),
                language=movie_dict.get("language"),
                rating=movie_dict.get("rating"),
                cast_info=movie_dict.get("cast_info"),
                genres=genres_val,
                ott_providers=ott_val,
            )
            await watchlist_svc.add_to_watchlist(movie, auto_download=True)
            await self._reload_watchlist()
        except Exception as e:
            logger.error(f"Failed to add to watchlist: {e}")

    # --- Search View Event Handlers ---
    @rx.event(background=True)
    async def run_search(self, form_data: dict = None):
        async with self:
            if form_data:
                # Extract query and year if passed via form
                if "search_query" in form_data:
                    self.search_query = form_data["search_query"]
                if "search_year" in form_data:
                    self.search_year = form_data["search_year"]

            if not self.search_query.strip():
                return

            self.search_loading = True
            self.search_error = ""
            self.search_results = []
        yield

        async with self:
            query = self.search_query.strip()

        # Check if it is direct JioSaavn Link
        import re

        jiosaavn_match = re.search(r"jiosaavn\.com/album/[^/]+/([a-zA-Z0-9_-]+)", query)
        if jiosaavn_match:
            try:
                album_id = jiosaavn_match.group(1)
                soundtrack_svc = SoundtrackService()
                album = await soundtrack_svc.get_album_details(album_id)
                if not album:
                    raise Exception("JioSaavn album not found.")

                movie = Movie(
                    source="jiosaavn",
                    source_id=album_id,
                    title=album.title,
                    year=None,
                    poster_url=album.cover_url,
                    overview=f"Direct JioSaavn link: {album.title} by {album.artist}",
                )
                async with self:
                    self.search_loading = False
                    self.selected_movie = to_dict(movie)
                    self.selected_album = to_dict(album)
                    self.show_songs_view = True
                yield
                yield AppState.bg_load_album_tracks
            except Exception as e:
                logger.error(f"Error resolving JioSaavn link: {e}")
                async with self:
                    self.search_error = f"JioSaavn link error: {e}"
                    self.search_loading = False
            return

        # Check if it is direct Spotify Link (album or track)
        spotify_match = re.search(r"spotify\.com/(album|track)/([a-zA-Z0-9]+)", query)
        if spotify_match:
            try:
                from movie_song_downloader.providers.spotify_provider import (
                    SpotifyProvider,
                )

                spotify_prov = SpotifyProvider()
                movie, album, tracks = await spotify_prov.get_spotify_album_or_track(
                    query
                )
                async with self:
                    self.search_loading = False
                    self.selected_movie = to_dict(movie)
                    self.selected_album = to_dict(album)
                    self.show_songs_view = True
                yield
                yield AppState.bg_load_album_tracks
            except Exception as e:
                logger.error(f"Error resolving Spotify link: {e}")
                async with self:
                    self.search_error = f"Spotify link error: {e}"
                    self.search_loading = False
            return

        # Regular Wikipedia Search
        async with self:
            search_year_val = self.search_year.strip()
        year_val = None
        if search_year_val:
            try:
                year_val = int(search_year_val)
            except ValueError:
                pass

        try:
            movie_svc = MovieService()
            movies = await movie_svc.search_movies(query, year=year_val)
            async with self:
                self.search_results = [to_dict(m) for m in movies]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            async with self:
                self.search_error = f"Search failed: {e}"
                self.search_results = []

        async with self:
            self.search_loading = False

    # --- Songs View Event Handlers ---
    @rx.event(background=True)
    async def on_browse_clicked(self, movie_dict: dict):
        async with self:
            self.selected_movie = movie_dict
            self.show_songs_view = True
            self.album_tracks = []
            self.tracks_loading = True
        yield

        try:
            soundtrack_svc = SoundtrackService()
            year = movie_dict.get("year")
            m_id = movie_dict.get("id")
            albums = await soundtrack_svc.find_soundtracks(
                movie_dict["title"], year, movie_id=m_id
            )
            if not albums:
                async with self:
                    self.selected_album = {}
                    self.album_tracks = []
                    self.tracks_loading = False
            else:
                best_album = albums[0]
                async with self:
                    self.selected_album = to_dict(best_album)
                yield
                yield AppState.bg_load_album_tracks
        except Exception as e:
            logger.error(f"Failed browsing soundtracks: {e}")
            async with self:
                self.tracks_loading = False

    async def load_album_tracks(self):
        self.tracks_loading = True
        self.album_tracks = []
        self.selected_track_ids = []
        yield

        album_id = self.selected_album.get("id")
        source_id = self.selected_album.get("source_id")

        # Ensure Cover Art is cached in background
        cover_url = self.selected_album.get("cover_url")
        cover_cached = self.selected_album.get("cover_cached_path")
        if cover_url and not cover_cached:
            try:
                from movie_song_downloader.core.cache_manager import image_cache

                cached = await image_cache.get_or_download(cover_url, "cover")
                if cached:
                    self.selected_album["cover_cached_path"] = cached
                    conn = await db.get_connection()
                    try:
                        await conn.execute(
                            "UPDATE albums SET cover_cached_path = ? WHERE source_id = ?",
                            (cached, source_id),
                        )
                        await conn.commit()
                    finally:
                        await conn.close()
            except Exception as ce:
                logger.error(f"Error caching cover art: {ce}")

        try:
            soundtrack_svc = SoundtrackService()
            tracks = await soundtrack_svc.get_tracks_for_album(
                source_id, db_album_id=album_id
            )

            serialized_tracks = []
            for t in tracks:
                track_db_id = await self._ensure_metadata_in_db(t)
                t_dict = to_dict(t)
                t_dict["db_id"] = track_db_id
                serialized_tracks.append(t_dict)

            self.album_tracks = serialized_tracks
            self.selected_track_ids = [t["db_id"] for t in serialized_tracks]
            self.select_all = True
        except Exception as e:
            logger.error(f"Error loading tracks: {e}")
            self.album_tracks = []

        self.tracks_loading = False

    @rx.event(background=True)
    async def bg_load_album_tracks(self):
        """Background wrapper for load_album_tracks to allow non-blocking track loading."""
        async with self:
            self.tracks_loading = True
            self.album_tracks = []
            self.selected_track_ids = []
        yield

        async with self:
            album_id = self.selected_album.get("id")
            source_id = self.selected_album.get("source_id")
            cover_url = self.selected_album.get("cover_url")
            cover_cached = self.selected_album.get("cover_cached_path")

        if cover_url and not cover_cached:
            try:
                from movie_song_downloader.core.cache_manager import image_cache
                cached = await image_cache.get_or_download(cover_url, "cover")
                if cached:
                    async with self:
                        self.selected_album["cover_cached_path"] = cached
                    conn = await db.get_connection()
                    try:
                        await conn.execute(
                            "UPDATE albums SET cover_cached_path = ? WHERE source_id = ?",
                            (cached, source_id),
                        )
                        await conn.commit()
                    finally:
                        await conn.close()
            except Exception as ce:
                logger.error(f"Error caching cover art: {ce}")

        try:
            soundtrack_svc = SoundtrackService()
            tracks = await soundtrack_svc.get_tracks_for_album(
                source_id, db_album_id=album_id
            )

            serialized_tracks = []
            for t in tracks:
                track_db_id = await self._ensure_metadata_in_db(t)
                t_dict = to_dict(t)
                t_dict["db_id"] = track_db_id
                serialized_tracks.append(t_dict)

            async with self:
                self.album_tracks = serialized_tracks
                self.selected_track_ids = [t["db_id"] for t in serialized_tracks]
                self.select_all = True
        except Exception as e:
            logger.error(f"Error loading tracks: {e}")
            async with self:
                self.album_tracks = []

        async with self:
            self.tracks_loading = False

    async def _ensure_metadata_in_db(self, track: Track) -> int:
        conn = await db.get_connection()
        try:
            # 1. Ensure Movie Record is saved
            async with conn.execute(
                "SELECT id FROM movies WHERE source_id=? AND source=?",
                (
                    self.selected_movie.get("source_id"),
                    self.selected_movie.get("source"),
                ),
            ) as cursor:
                movie_row = await cursor.fetchone()
                if movie_row:
                    movie_id = movie_row[0]
                else:
                    async with conn.execute(
                        "SELECT id FROM movies WHERE title=? AND year=?",
                        (
                            self.selected_movie.get("title"),
                            self.selected_movie.get("year"),
                        ),
                    ) as c2:
                        r2 = await c2.fetchone()
                        if r2:
                            movie_id = r2[0]
                        else:
                            genres_val = self.selected_movie.get("genres", [])
                            if isinstance(genres_val, list):
                                genres_val = json.dumps(genres_val)
                            ott_val = self.selected_movie.get("ott_providers", [])
                            if isinstance(ott_val, list):
                                ott_val = json.dumps(ott_val)

                            tmdb_id = self.selected_movie.get("tmdb_id", 0)
                            if tmdb_id == 0 or tmdb_id is None:
                                import hashlib

                                title_val = self.selected_movie.get("title")
                                srcid_val = self.selected_movie.get("source_id") or ""
                                hash_input = f"{title_val}|{srcid_val}"
                                tmdb_id = int(
                                    hashlib.md5(hash_input.encode("utf-8")).hexdigest()
                                    [:8],
                                    16,
                                )

                            m_cursor = await conn.execute(
                                (
                                    "INSERT INTO movies (tmdb_id, source, "
                                    "source_id, title, year, poster_url, "
                                    "overview, language, genres, ott_providers, "
                                    "rating, cast_info) "
                                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                                ),
                                (
                                    tmdb_id,
                                    self.selected_movie.get("source", "wikipedia"),
                                    self.selected_movie.get("source_id", ""),
                                    self.selected_movie.get("title"),
                                    self.selected_movie.get("year"),
                                    self.selected_movie.get("poster_url"),
                                    self.selected_movie.get("overview"),
                                    self.selected_movie.get("language"),
                                    genres_val,
                                    ott_val,
                                    self.selected_movie.get("rating"),
                                    self.selected_movie.get("cast_info"),
                                ),
                            )
                            movie_id = m_cursor.lastrowid

            # 2. Ensure Album Record is saved
            album_id = self.selected_album.get("id")
            async with conn.execute(
                "SELECT id FROM albums WHERE source_id=? AND source=?",
                (
                    self.selected_album.get("source_id"),
                    self.selected_album.get("source"),
                ),
            ) as cursor:
                album_row = await cursor.fetchone()
                if album_row:
                    album_id = album_row[0]
                    self.selected_album["id"] = album_id
                else:
                    a_cursor = await conn.execute(
                        (
                            "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, artist, "
                            "cover_url, total_tracks) VALUES (?,?,?,?,?,?,?,?)"
                        ),
                        (
                            movie_id,
                            self.selected_album.get("spotify_id"),
                            self.selected_album.get("source", "jiosaavn"),
                            self.selected_album.get("source_id"),
                            self.selected_album.get("title"),
                            self.selected_album.get("artist"),
                            self.selected_album.get("cover_url"),
                            self.selected_album.get("total_tracks"),
                        ),
                    )
                    album_id = a_cursor.lastrowid
                    self.selected_album["id"] = album_id

            # 3. Ensure Track Record is saved
            async with conn.execute(
                "SELECT id FROM tracks WHERE source_id=? AND source=?",
                (track.source_id, track.source),
            ) as cursor:
                track_row = await cursor.fetchone()
                if track_row:
                    track_id = track_row[0]
                else:
                    t_cursor = await conn.execute(
                        (
                            "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, "
                            "duration_ms, track_number, preview_url, download_url) VALUES (?,?,?,?,?,?,?,?,?,?)"
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
                        ),
                    )
                    track_id = t_cursor.lastrowid

            await conn.commit()
            return track_id
        finally:
            await conn.close()

    def toggle_select_all(self):
        self.select_all = not self.select_all
        if self.select_all:
            self.selected_track_ids = [t["db_id"] for t in self.album_tracks]
        else:
            self.selected_track_ids = []

    def toggle_track_selection(self, db_id: int):
        if db_id in self.selected_track_ids:
            self.selected_track_ids.remove(db_id)
        else:
            self.selected_track_ids.append(db_id)
        self.select_all = len(self.selected_track_ids) == len(self.album_tracks)

    def play_preview_clip(self, url: str):
        if self.audio_preview_url == url:
            self.audio_preview_url = ""  # Stop
        else:
            self.audio_preview_url = url

    @rx.event(background=True)
    async def download_selected_tracks(self):
        if not self.selected_track_ids:
            return

        async with self:
            self.download_btn_text = "Checking Path..."
            self.download_btn_disabled = True
        yield

        path = await settings_manager.get("output_dir")
        if not path or not path.strip():
            # Show Dialog picker required
            async with self:
                self.pending_download_track_ids = list(self.selected_track_ids)
                self.missing_dir_dialog_open = True
                self.download_btn_text = "Download Selected"
                self.download_btn_disabled = False
        else:
            async with self:
                self.download_btn_text = "Queuing..."
            yield
            await self._enqueue_tracks(self.selected_track_ids)
            await asyncio.sleep(1.0)
            async with self:
                self.download_btn_text = "Download Selected"
                self.download_btn_disabled = False

    async def _enqueue_tracks(self, track_ids: list[int]):
        audio_format_val = await settings_manager.get("audio_format") or "mp3"
        for t_id in track_ids:
            try:
                await job_queue.enqueue(t_id, format=audio_format_val)
            except Exception as e:
                logger.error(f"Error enqueuing track {t_id}: {e}")

    def close_songs_view(self):
        self.show_songs_view = False
        self.audio_preview_url = ""

    # --- Missing Directory Dialog Handlers ---
    def close_missing_dir_dialog(self):
        self.missing_dir_dialog_open = False
        self.pending_download_track_ids = []

    def trigger_dialog_folder_picker(self):
        self.missing_dir_dialog_open = False
        return self.open_dir_explorer("dialog_download")

    # --- Directory Explorer Event Handlers ---
    def open_dir_explorer(self, target_key: str = "output_dir"):
        self.dir_target_setting = target_key
        self.dir_explorer_open = True
        self.dir_explorer_error = ""

        path = self.output_dir
        if not path or not os.path.exists(path):
            path = str(Path.home() / "Music" / "movie_song_downloader")

        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        self.dir_explorer_path = os.path.abspath(path)
        self._refresh_dir_items()

    def navigate_dir(self, sub_dir: str):
        new_path = os.path.join(self.dir_explorer_path, sub_dir)
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.dir_explorer_path = os.path.abspath(new_path)
            self._refresh_dir_items()

    def navigate_up_dir(self):
        parent_path = os.path.dirname(self.dir_explorer_path)
        # Prevent navigating past drive root
        if os.path.exists(parent_path) and os.path.isdir(parent_path):
            self.dir_explorer_path = os.path.abspath(parent_path)
            self._refresh_dir_items()

    def _refresh_dir_items(self):
        try:
            items = []
            for item in os.listdir(self.dir_explorer_path):
                full_path = os.path.join(self.dir_explorer_path, item)
                if os.path.isdir(full_path):
                    if not item.startswith(".") and not item.startswith("$"):
                        items.append(item)
            self.dir_explorer_items = sorted(items, key=lambda s: s.lower())
            self.dir_explorer_error = ""
        except Exception as e:
            self.dir_explorer_error = f"Error reading folder: {e}"
            self.dir_explorer_items = []

    async def select_current_dir(self):
        chosen_dir = self.dir_explorer_path
        self.dir_explorer_open = False

        if self.dir_target_setting == "dialog_download":
            # Save and then run enqueued tasks
            await settings_manager.set("output_dir", chosen_dir)
            self.output_dir = chosen_dir
            yield
            await self._enqueue_tracks(self.pending_download_track_ids)
            self.pending_download_track_ids = []
        else:
            self.output_dir = chosen_dir
            # We don't save to settings until "Save Settings" clicked, or we can save directly.
            # In Flet settings_view, settings were saved when user clicked "Save Settings".
            # We will follow that.

    async def cancel_dir_explorer(self):
        self.dir_explorer_open = False
        if self.dir_target_setting == "dialog_download":
            # Default to Downloads directory and proceed
            downloads_dir = str(Path.home() / "Downloads")
            await settings_manager.set("output_dir", downloads_dir)
            self.output_dir = downloads_dir
            yield
            await self._enqueue_tracks(self.pending_download_track_ids)
            self.pending_download_track_ids = []

    # --- Downloads View Handlers ---
    @rx.event(background=True)
    async def load_download_jobs(self):
        async with self:
            self.downloads_loading = True
        yield
        try:
            jobs = await job_queue.get_all_jobs()
            serialized = []
            for j in jobs:
                d = to_dict(j)
                d["status"] = d["status"].lower() if d.get("status") else "queued"
                serialized.append(d)
            async with self:
                self.download_jobs = serialized
        except Exception as e:
            logger.error(f"Failed loading download jobs: {e}")
            async with self:
                self.download_jobs = []
        async with self:
            self.downloads_loading = False

    async def cancel_download_job(self, job_id: int):
        try:
            await job_queue.cancel(job_id)
            async for event in self.load_download_jobs():
                yield event
        except Exception as e:
            logger.error(f"Error cancelling job {job_id}: {e}")

    async def resume_download_job(self, job_id: int):
        try:
            await job_queue.resume(job_id)
            async for event in self.load_download_jobs():
                yield event
        except Exception as e:
            logger.error(f"Error resuming job {job_id}: {e}")

    async def retry_download_job(self, job_id: int):
        try:
            await job_queue.resume(job_id)
            async for event in self.load_download_jobs():
                yield event
        except Exception as e:
            logger.error(f"Error retrying job {job_id}: {e}")

    # Background event handler to poll downloads periodically
    @rx.event(background=True)
    async def start_polling(self):
        while True:
            await asyncio.sleep(1.0)
            async with self:
                if self.active_tab != "downloads" or self.downloads_loading:
                    continue
                try:
                    jobs = await job_queue.get_all_jobs()
                    serialized = []
                    for j in jobs:
                        d = to_dict(j)
                        d["status"] = d["status"].upper()
                        serialized.append(d)
                    self.download_jobs = serialized
                except Exception as e:
                    logger.error(f"Polling jobs error: {e}")

    # --- Settings View Handlers ---
    async def load_settings(self):
        try:
            data = await settings_manager.get_all()
            self.omdb_api_key = data.get("omdb_api_key", "")
            self.deezer_arl = data.get("deezer_arl", "")
            self.output_dir = data.get("output_dir", "")

            folder_val = data.get("folder_format", "")
            filename_val = data.get("filename_format", "")

            folder_presets = [
                "{Year}/{Movie}/Songs",
                "{Movie}",
                "{Artist}/{Album}",
                "{Movie}/{Songs}",
            ]
            if folder_val in folder_presets:
                self.folder_format_dropdown = folder_val
                self.folder_format_custom = folder_val
            else:
                self.folder_format_dropdown = "Custom..."
                self.folder_format_custom = folder_val

            filename_presets = [
                "{TrackNum} - {Title}",
                "{Title}",
                "{Artist} - {Title}",
                "{TrackNum}. {Title}",
            ]
            if filename_val in filename_presets:
                self.filename_format_dropdown = filename_val
                self.filename_format_custom = filename_val
            else:
                self.filename_format_dropdown = "Custom..."
                self.filename_format_custom = filename_val

            self.audio_format = data.get("audio_format", "mp3")
            self.bitrate = data.get("bitrate", "320")

            self.save_lrc_file = data.get("save_lrc_file", "true") == "true"
            self.embed_lyrics = data.get("embed_lyrics", "true") == "true"
            self.auto_download = data.get("auto_download", "true") == "true"

            # Load download provider setting
            self.download_provider = data.get("download_provider", "spotiflac")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")

    async def save_settings(self):
        self.settings_status_msg = "Saving..."
        self.settings_status_color = "#F59E0B"
        yield

        try:
            folder_to_save = self.folder_format_custom
            if self.folder_format_dropdown != "Custom...":
                folder_to_save = self.folder_format_dropdown

            filename_to_save = self.filename_format_custom
            if self.filename_format_dropdown != "Custom...":
                filename_to_save = self.filename_format_dropdown

            settings_map = {
                "omdb_api_key": self.omdb_api_key,
                "deezer_arl": self.deezer_arl,
                "output_dir": self.output_dir,
                "folder_format": folder_to_save or "{Year}/{Movie}/Songs",
                "filename_format": filename_to_save or "{TrackNum} - {Title}",
                "audio_format": self.audio_format or "mp3",
                "bitrate": self.bitrate or "320",
                "save_lrc_file": "true" if self.save_lrc_file else "false",
                "embed_lyrics": "true" if self.embed_lyrics else "false",
                "auto_download": "true" if self.auto_download else "false",
                "download_provider": self.download_provider or "spotiflac",
            }
            await settings_manager.save_many(settings_map)
            self.settings_status_msg = "Settings Saved Successfully!"
            self.settings_status_color = "#22C55E"
        except Exception as e:
            self.settings_status_msg = f"Failed to save settings: {e}"
            self.settings_status_color = "#EF4444"

    # --- First-run Setup Wizard Handlers ---
    async def _check_first_run(self):
        omdb_key = await settings_manager.get("omdb_api_key")
        if not omdb_key:
            self.setup_wizard_open = True
            self.setup_omdb_key = ""
            self.setup_deezer_arl = ""
            self.setup_status_msg = ""

    async def save_setup_wizard(self):
        if not self.setup_omdb_key.strip():
            self.setup_status_msg = (
                "OMDb API Key is required! Get a free key from omdbapi.com"
            )
            return

        yield
        try:
            await settings_manager.set("omdb_api_key", self.setup_omdb_key.strip())
            if self.setup_deezer_arl.strip():
                await settings_manager.set("deezer_arl", self.setup_deezer_arl.strip())
            self.setup_wizard_open = False
            await self.load_settings()
        except Exception as e:
            self.setup_status_msg = f"Error saving keys: {e}"

    # --- Custom Setters for UI Inputs (Bypass dynamic metaclass issues) ---
    def set_search_query(self, val: str):
        self.search_query = val

    def set_search_year(self, val: str):
        self.search_year = val

    def set_omdb_api_key(self, val: str):
        self.omdb_api_key = val

    def set_deezer_arl(self, val: str):
        self.deezer_arl = val

    def set_folder_format_dropdown(self, val: str):
        self.folder_format_dropdown = val

    def set_folder_format_custom(self, val: str):
        self.folder_format_custom = val

    def set_filename_format_dropdown(self, val: str):
        self.filename_format_dropdown = val

    def set_filename_format_custom(self, val: str):
        self.filename_format_custom = val

    def set_audio_format(self, val: str):
        self.audio_format = val

    def set_bitrate(self, val: str):
        self.bitrate = val

    def set_save_lrc_file(self, val: bool):
        self.save_lrc_file = val

    def set_embed_lyrics(self, val: bool):
        self.embed_lyrics = val

    def set_auto_download(self, val: bool):
        self.auto_download = val

    def set_setup_omdb_key(self, val: str):
        self.setup_omdb_key = val

    def set_setup_deezer_arl(self, val: str):
        self.setup_deezer_arl = val

    def set_download_provider(self, val: str):
        self.download_provider = val
