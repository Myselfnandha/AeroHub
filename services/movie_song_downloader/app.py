# ruff: noqa: E402, F401
# movie_song_downloader/app.py
from contextlib import asynccontextmanager
import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, List
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

# Resolve path directory
import sys
sub_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(sub_dir))
services_dir = os.path.join(workspace_root, "services")

if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Register Redirector for package naming compatibility
from importlib.abc import MetaPathFinder
import importlib
class MovieSongDownloaderRedirector(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("MovieSongDownloader"):
            real_name = fullname.replace("MovieSongDownloader", "movie_song_downloader", 1)
            mod = importlib.import_module(real_name)
            sys.modules[fullname] = mod
            return mod.__spec__
        return None

if not any(isinstance(f, MovieSongDownloaderRedirector) for f in sys.meta_path):
    sys.meta_path.insert(0, MovieSongDownloaderRedirector())

from movie_song_downloader.core.database import db
from movie_song_downloader.core.models import Movie, Track, Album
from movie_song_downloader.services.movie_service import MovieService
from movie_song_downloader.services.soundtrack_service import SoundtrackService
from movie_song_downloader.services.watchlist_service import WatchlistService
from movie_song_downloader.services.download_service import download_service
from movie_song_downloader.core.settings_manager import settings_manager
from movie_song_downloader.core.job_queue import job_queue

logger = logging.getLogger("movie_song_downloader.FastAPI")

def to_dict(obj):
    if not obj:
        return {}
    return asdict(obj)

# Global background fetching state
fetching_state = {
    "is_fetching": False,
    "status": "Idle",
    "progress": 0.0,
    "new_movies": []
}

async def bg_progress_cb(pct: float, msg: str = ""):
    fetching_state["progress"] = pct
    if msg:
        fetching_state["status"] = msg

async def run_bg_fetch():
    fetching_state["is_fetching"] = True
    fetching_state["progress"] = 0.0
    fetching_state["status"] = "Checking for updates..."
    fetching_state["new_movies"] = []
    try:
        movie_svc = MovieService()
        new_movies = await movie_svc.get_today_releases("IN", on_progress=bg_progress_cb)
        fetching_state["new_movies"] = [to_dict(m) for m in new_movies]
        fetching_state["progress"] = 100.0
        fetching_state["status"] = "Finished checking for updates."
    except Exception as e:
        fetching_state["status"] = f"Error: {str(e)}"
        fetching_state["progress"] = 100.0
        logger.error(f"Background updates error: {e}")
    finally:
        fetching_state["is_fetching"] = False

async def progress_stream():
    while True:
        status = fetching_state["status"]
        progress = fetching_state["progress"]
        is_fetching = fetching_state["is_fetching"]
        
        data = json.dumps({
            "is_fetching": is_fetching,
            "status": status,
            "progress": progress,
            "has_new_movies": len(fetching_state["new_movies"]) > 0
        })
        yield f"data: {data}\n\n"
        
        if not is_fetching and progress >= 100.0:
            break
        await asyncio.sleep(0.5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Starting up FastAPI application...")
    try:
        await db.run_migrations()
        logger.info("Database migrations run successfully.")
    except Exception as e:
        logger.error(f"Failed to run database migrations: {e}")
    
    try:
        await download_service.start()
        logger.info("Background download service worker started.")
    except Exception as e:
        logger.error(f"Failed to start download service worker: {e}")
        
    yield
    
    # Shutdown tasks
    logger.info("Shutting down FastAPI application...")
    try:
        await download_service.stop()
        logger.info("Background download service worker stopped.")
    except Exception as e:
        logger.error(f"Error stopping download worker: {e}")

app = FastAPI(lifespan=lifespan)

# Define static directories
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Mount JS static folder
app.mount("/js", StaticFiles(directory=os.path.join(static_dir, "js")), name="js")

# Mount assets if they exist
assets_dir = os.path.join(static_dir, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Serve visual styles directly
@app.get("/style.css")
async def get_style():
    return FileResponse(os.path.join(static_dir, "css", "style.css"))

# --- Clean Page Routes ---
@app.get("/")
async def get_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/search")
async def get_search():
    return FileResponse(os.path.join(static_dir, "search.html"))

@app.get("/songs")
async def get_songs():
    return FileResponse(os.path.join(static_dir, "songs.html"))

@app.get("/watchlist")
async def get_watchlist_page():
    return FileResponse(os.path.join(static_dir, "watchlist.html"))

@app.get("/downloads")
async def get_downloads_page():
    return FileResponse(os.path.join(static_dir, "downloads.html"))

@app.get("/settings")
async def get_settings_page():
    return FileResponse(os.path.join(static_dir, "settings.html"))

# --- API Routes ---

# 1. Settings Endpoints
@app.get("/api/settings")
async def get_settings():
    try:
        data = await settings_manager.get_all()
        return {
            "omdb_api_key": data.get("omdb_api_key", ""),
            "deezer_arl": data.get("deezer_arl", ""),
            "output_dir": data.get("output_dir", ""),
            "folder_format": data.get("folder_format", "{Year}/{Movie}/Songs"),
            "filename_format": data.get("filename_format", "{TrackNum} - {Title}"),
            "audio_format": data.get("audio_format", "mp3"),
            "bitrate": data.get("bitrate", "320"),
            "download_provider": data.get("download_provider", "spotiflac"),
            "save_lrc_file": data.get("save_lrc_file", "true") == "true",
            "embed_lyrics": data.get("embed_lyrics", "true") == "true",
            "auto_download": data.get("auto_download", "true") == "true",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings")
async def save_settings(payload: dict):
    try:
        settings_map = {}
        for k, v in payload.items():
            if isinstance(v, bool):
                settings_map[k] = "true" if v else "false"
            else:
                settings_map[k] = str(v)
        await settings_manager.save_many(settings_map)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings/set-default-dir")
async def set_default_dir():
    try:
        downloads_dir = str(Path.home() / "Downloads")
        await settings_manager.set("output_dir", downloads_dir)
        return {"status": "ok", "output_dir": downloads_dir}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Movie & Search Endpoints
@app.get("/api/movies/cached")
async def get_cached_movies():
    try:
        movie_svc = MovieService()
        movies = await movie_svc.get_cached_releases()
        return [to_dict(m) for m in movies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/movies/fetch-updates")
async def fetch_updates(background_tasks: BackgroundTasks):
    if fetching_state["is_fetching"]:
        return {"status": "already_fetching"}
    background_tasks.add_task(run_bg_fetch)
    return {"status": "started"}

@app.get("/api/movies/fetch-progress")
async def fetch_progress():
    return StreamingResponse(progress_stream(), media_type="text/event-stream")

@app.post("/api/movies/apply-updates")
async def apply_updates():
    fetching_state["new_movies"] = []
    fetching_state["progress"] = 0.0
    fetching_state["status"] = "Idle"
    return {"status": "ok"}

@app.post("/api/movies/search")
async def search_movies(q: str = Query(...), year: Optional[str] = Query(None)):
    query = q.strip()
    import re
    
    # JioSaavn link check
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
            # Find or save in DB
            conn = await db.get_connection()
            try:
                # Ensure movie record
                async with conn.execute(
                    "SELECT id FROM movies WHERE source_id=? AND source=?", (album_id, "jiosaavn")
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        movie.id = row[0]
                    else:
                        m_cursor = await conn.execute(
                            "INSERT INTO movies (source, source_id, title, poster_url, overview) VALUES (?,?,?,?,?)",
                            ("jiosaavn", album_id, album.title, album.cover_url, movie.overview)
                        )
                        movie.id = m_cursor.lastrowid
                        await conn.commit()
                # Ensure album record
                async with conn.execute(
                    "SELECT id FROM albums WHERE source_id=? AND source=?", (album_id, "jiosaavn")
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        album.id = row[0]
                    else:
                        a_cursor = await conn.execute(
                            "INSERT INTO albums (movie_id, source, source_id, title, artist, cover_url, total_tracks) VALUES (?,?,?,?,?,?,?)",
                            (movie.id, "jiosaavn", album_id, album.title, album.artist, album.cover_url, album.total_tracks)
                        )
                        album.id = a_cursor.lastrowid
                        await conn.commit()
            finally:
                await conn.close()
                
            return {
                "type": "redirect",
                "movie": to_dict(movie),
                "album": to_dict(album)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"JioSaavn link error: {str(e)}")
            
    # Spotify link check
    spotify_match = re.search(r"spotify\.com/(album|track)/([a-zA-Z0-9]+)", query)
    if spotify_match:
        try:
            from movie_song_downloader.providers.spotify_provider import SpotifyProvider
            spotify_prov = SpotifyProvider()
            movie, album, tracks = await spotify_prov.get_spotify_album_or_track(query)
            
            # Save records
            conn = await db.get_connection()
            try:
                async with conn.execute(
                    "SELECT id FROM movies WHERE source_id=? AND source=?", (movie.source_id, movie.source)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        movie.id = row[0]
                    else:
                        m_cursor = await conn.execute(
                            "INSERT INTO movies (source, source_id, title, year, poster_url, overview) VALUES (?,?,?,?,?,?)",
                            (movie.source, movie.source_id, movie.title, movie.year, movie.poster_url, movie.overview)
                        )
                        movie.id = m_cursor.lastrowid
                        await conn.commit()
                        
                async with conn.execute(
                    "SELECT id FROM albums WHERE source_id=? AND source=?", (album.source_id, album.source)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        album.id = row[0]
                    else:
                        a_cursor = await conn.execute(
                            "INSERT INTO albums (movie_id, source, source_id, title, artist, cover_url, total_tracks) VALUES (?,?,?,?,?,?,?)",
                            (movie.id, album.source, album.source_id, album.title, album.artist, album.cover_url, album.total_tracks)
                        )
                        album.id = a_cursor.lastrowid
                        await conn.commit()
            finally:
                await conn.close()
                
            return {
                "type": "redirect",
                "movie": to_dict(movie),
                "album": to_dict(album)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Spotify link error: {str(e)}")
            
    # Normal search
    year_val = None
    if year:
        try:
            year_val = int(year)
        except ValueError:
            pass
    try:
        movie_svc = MovieService()
        movies = await movie_svc.search_movies(query, year=year_val)
        return {
            "type": "results",
            "results": [to_dict(m) for m in movies]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/browse")
async def browse_movie(
    movie_id: Optional[str] = None,
    source: str = "wikipedia",
    source_id: str = "",
    title: str = "",
    year: Optional[str] = None,
    album_source_id: Optional[str] = None
):
    year_val = None
    if year:
        try:
            year_val = int(year)
        except ValueError:
            pass
            
    movie_dict = {
        "id": int(movie_id) if movie_id else None,
        "source": source,
        "source_id": source_id,
        "title": title,
        "year": year_val,
        "poster_url": "",
        "overview": "",
        "rating": None
    }
    
    conn = await db.get_connection()
    try:
        if not movie_dict["id"]:
            async with conn.execute(
                "SELECT id, poster_url, overview, rating FROM movies WHERE source_id=? AND source=?",
                (source_id, source)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    movie_dict["id"] = row[0]
                    movie_dict["poster_url"] = row[1] or ""
                    movie_dict["overview"] = row[2] or ""
                    movie_dict["rating"] = row[3]
        
        soundtrack_svc = SoundtrackService()
        albums = []
        if album_source_id:
            album = await soundtrack_svc.get_album_details(album_source_id)
            if album:
                albums = [album]
        else:
            albums = await soundtrack_svc.find_soundtracks(title, year_val, movie_id=movie_dict["id"])
            
        if not albums:
            return {
                "movie": movie_dict,
                "album": {},
                "tracks": []
            }
            
        best_album = albums[0]
        
        # Ensure movie and album are in DB
        db_movie_id = movie_dict["id"]
        if not db_movie_id:
            m_cursor = await conn.execute(
                "INSERT INTO movies (source, source_id, title, year, poster_url, overview) VALUES (?,?,?,?,?,?)",
                (source, source_id, title, year_val, movie_dict.get("poster_url"), movie_dict.get("overview"))
            )
            db_movie_id = m_cursor.lastrowid
            movie_dict["id"] = db_movie_id
            await conn.commit()
            
        db_album_id = best_album.id
        async with conn.execute(
            "SELECT id FROM albums WHERE source_id=? AND source=?",
            (best_album.source_id, best_album.source)
        ) as cursor:
            album_row = await cursor.fetchone()
            if album_row:
                db_album_id = album_row[0]
                best_album.id = db_album_id
            else:
                a_cursor = await conn.execute(
                    "INSERT INTO albums (movie_id, spotify_id, source, source_id, title, artist, cover_url, total_tracks) VALUES (?,?,?,?,?,?,?,?)",
                    (db_movie_id, best_album.spotify_id, best_album.source or "jiosaavn", best_album.source_id, best_album.title, best_album.artist, best_album.cover_url, best_album.total_tracks)
                )
                db_album_id = a_cursor.lastrowid
                best_album.id = db_album_id
                await conn.commit()
                
        # Load tracks
        tracks = await soundtrack_svc.get_tracks_for_album(best_album.source_id, db_album_id=db_album_id)
        
        serialized_tracks = []
        for t in tracks:
            track_db_id = None
            async with conn.execute(
                "SELECT id FROM tracks WHERE source_id=? AND source=?",
                (t.source_id, t.source)
            ) as cursor:
                t_row = await cursor.fetchone()
                if t_row:
                    track_db_id = t_row[0]
                else:
                    t_cursor = await conn.execute(
                        "INSERT INTO tracks (album_id, spotify_id, source, source_id, title, artist, duration_ms, track_number, preview_url, download_url) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (db_album_id, t.spotify_id, t.source, t.source_id, t.title, t.artist, t.duration_ms, t.track_number, t.preview_url, t.download_url)
                    )
                    track_db_id = t_cursor.lastrowid
                    await conn.commit()
            t_dict = to_dict(t)
            t_dict["db_id"] = track_db_id
            serialized_tracks.append(t_dict)
            
        return {
            "movie": movie_dict,
            "album": to_dict(best_album),
            "tracks": serialized_tracks
        }
    finally:
        await conn.close()

# 3. Watchlist Endpoints
@app.get("/api/watchlist")
async def get_watchlist():
    try:
        watchlist_svc = WatchlistService()
        items = await watchlist_svc.get_watchlist()
        return [to_dict(i) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/watchlist")
async def add_watchlist(payload: dict):
    try:
        watchlist_svc = WatchlistService()
        movie = Movie(
            source=payload.get("source", "wikipedia"),
            source_id=payload.get("source_id", ""),
            title=payload.get("title", ""),
            year=payload.get("year"),
        )
        await watchlist_svc.add_to_watchlist(movie, auto_download=payload.get("auto_download", True))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/watchlist/{id}")
async def remove_watchlist_item(id: int):
    conn = await db.get_connection()
    try:
        await conn.execute("DELETE FROM watchlist WHERE id=?", (id,))
        await conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()

@app.post("/api/watchlist/check")
async def check_watchlist():
    try:
        watchlist_svc = WatchlistService()
        await watchlist_svc.check_releases_and_trigger()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Downloads & Queue Endpoints
@app.get("/api/downloads")
async def get_downloads():
    try:
        jobs = await job_queue.get_all_jobs()
        return [to_dict(j) for j in jobs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/downloads/enqueue")
async def enqueue_downloads(payload: dict):
    try:
        track_ids = payload.get("track_ids", [])
        audio_format_val = await settings_manager.get("audio_format") or "mp3"
        for t_id in track_ids:
            await job_queue.enqueue(t_id, format=audio_format_val)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/downloads/cancel/{id}")
async def cancel_job(id: int):
    try:
        await job_queue.cancel(id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/downloads/resume/{id}")
async def resume_job(id: int):
    try:
        await job_queue.resume(id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/downloads/retry/{id}")
async def retry_job(id: int):
    try:
        await job_queue.resume(id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Directory Explorer Utilities Endpoints
@app.get("/api/utils/dir-explorer")
async def dir_explorer(path: str = Query("")):
    try:
        if not path or not path.strip() or not os.path.exists(path):
            path = str(Path.home() / "Music" / "movie_song_downloader")
        
        os.makedirs(path, exist_ok=True)
        abs_path = os.path.abspath(path)
        
        parent_path = os.path.dirname(abs_path)
        if not os.path.exists(parent_path) or parent_path == abs_path:
            parent_path = ""
            
        items = []
        for item in os.listdir(abs_path):
            full_path = os.path.join(abs_path, item)
            if os.path.isdir(full_path):
                if not item.startswith(".") and not item.startswith("$"):
                    items.append(item)
                    
        return {
            "current_path": abs_path,
            "parent_path": parent_path,
            "subdirectories": sorted(items, key=lambda s: s.lower())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
