import os
import shutil
import asyncio
import logging
import json
from typing import Optional
from pathlib import Path
import httpx

from MovieSongDownloader.core.database import db
from MovieSongDownloader.core.models import DownloadJob, Movie, Album, Track
from MovieSongDownloader.core.job_queue import job_queue
from MovieSongDownloader.core.cache_manager import download_cache, image_cache
from MovieSongDownloader.core.settings_manager import settings_manager
from MovieSongDownloader.providers.deezspot_provider import DeezspotProvider
from MovieSongDownloader.providers.spotiflac_provider import SpotiFLACProvider
from MovieSongDownloader.providers.lyrics_provider import LyricsProvider
from MovieSongDownloader.providers.tagging_provider import TaggingProvider
from MovieSongDownloader.services.folder_service import FolderService

logger = logging.getLogger("MovieSongDownloader.DownloadService")


class DownloadService:
    def __init__(self):
        self.download_provider = DeezspotProvider()
        self.lyrics_provider = LyricsProvider()
        self.tagging_provider = TaggingProvider()
        self.folder_service = FolderService()
        self._worker_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("Download worker started.")

    async def stop(self) -> None:
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info("Download worker stopped.")

    async def _worker(self) -> None:
        while self._running:
            try:
                job = await job_queue.dequeue()
                if job:
                    task = asyncio.create_task(self._process(job))
                    await job_queue.register_task(job.id, task)
                    try:
                        await task
                    except asyncio.CancelledError:
                        await self._cleanup(job)
                    finally:
                        await job_queue.unregister_task(job.id)
                else:
                    await asyncio.sleep(2.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}", exc_info=True)
                await asyncio.sleep(5.0)

    async def _transcode_audio(
        self, input_path: str, output_path: str, format: str, bitrate: str = "320"
    ) -> None:
        # Locate local ffmpeg binary
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to system PATH

        format = format.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format == "flac":
            cmd.extend([output_path])
        elif format in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"Running transcode: {' '.join(cmd)}")

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def _process(self, job: DownloadJob) -> None:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT m.tmdb_id, m.title, m.year, m.poster_url, m.poster_cached_path, m.overview, "
                "m.language, m.genres, m.ott_providers, m.source, m.source_id, m.rating, m.cast_info "
                "FROM movies m JOIN albums a ON a.movie_id=m.id JOIN tracks t ON t.album_id=a.id "
                "WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                if not r:
                    await job_queue.mark_failed(job.id, "Movie/Album metadata missing.")
                    return
                movie = Movie(
                    tmdb_id=r[0],
                    title=r[1],
                    year=r[2],
                    poster_url=r[3],
                    poster_cached_path=r[4],
                    overview=r[5],
                    language=r[6],
                    genres=json.loads(r[7]) if r[7] else [],
                    ott_providers=json.loads(r[8]) if r[8] else [],
                    source=r[9],
                    source_id=r[10],
                    rating=r[11],
                    cast_info=r[12],
                )
            async with conn.execute(
                "SELECT a.id, a.spotify_id, a.title, a.artist, a.cover_url, a.cover_cached_path, "
                "a.total_tracks, a.source, a.source_id "
                "FROM albums a JOIN tracks t ON t.album_id=a.id WHERE t.id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                album = Album(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    cover_url=r[4],
                    cover_cached_path=r[5],
                    total_tracks=r[6],
                    source=r[7],
                    source_id=r[8],
                )
            async with conn.execute(
                "SELECT id, spotify_id, title, artist, duration_ms, track_number, preview_url, "
                "source, source_id, download_url FROM tracks WHERE id=?",
                (job.track_id,),
            ) as c:
                r = await c.fetchone()
                track = Track(
                    id=r[0],
                    spotify_id=r[1],
                    title=r[2],
                    artist=r[3],
                    duration_ms=r[4],
                    track_number=r[5],
                    preview_url=r[6],
                    source=r[7],
                    source_id=r[8],
                    download_url=r[9],
                )
        finally:
            await conn.close()

        # Cache dedup check
        track_hash = download_cache.generate_hash(
            track.artist, track.title, album.title, track.duration_ms
        )
        target_dir, abs_path = await self.folder_service.get_target_path(
            movie, album, track, job.format
        )
        hit = await download_cache.check(track_hash)

        if hit:
            await job_queue.update_progress(job.id, 50.0, "copying_from_cache")
            try:
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(hit["file_path"], abs_path)
                await self.folder_service.write_movie_metadata(movie, target_dir)
                await self.folder_service.generate_m3u_playlist(target_dir, album.title)
                await job_queue.mark_completed(job.id, abs_path)
                return
            except Exception as e:
                logger.error(f"Cache copy failed: {e}")

        # Download
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        await job_queue.update_progress(job.id, 10.0, "downloading")

        temp_path = None
        for attempt in range(3):
            temp_raw_path = None
            try:
                provider_setting = (
                    await settings_manager.get("download_provider") or "spotiflac"
                )
                use_cdn = (
                    track.download_url
                    and provider_setting != "spotiflac"
                    and job.format.lower() != "flac"
                )

                if use_cdn:
                    logger.info(
                        f"Downloading directly from JioSaavn CDN: {track.download_url}"
                    )
                    temp_raw_path = os.path.join(temp_dir, f"temp_{job.id}_raw.mp4")

                    async with httpx.AsyncClient(timeout=30.0) as client:
                        async with client.stream("GET", track.download_url) as resp:
                            if resp.status_code != 200:
                                raise Exception(
                                    f"Failed to fetch saavncdn URL: status {resp.status_code}"
                                )
                            total_bytes = int(resp.headers.get("content-length", 0))
                            downloaded_bytes = 0
                            with open(temp_raw_path, "wb") as f:
                                async for chunk in resp.iter_bytes(chunk_size=65536):
                                    f.write(chunk)
                                    downloaded_bytes += len(chunk)
                                    if total_bytes > 0:
                                        pct = (downloaded_bytes / total_bytes) * 100.0
                                        # Scale progress from 10% to 50% of the overall download pipeline
                                        scaled_prog = 10.0 + (pct / 100.0) * 40.0
                                        await job_queue.update_progress(
                                            job.id, scaled_prog, "downloading"
                                        )

                    bitrate = await settings_manager.get("bitrate") or "320"
                    dest_ext = job.format.lower()
                    temp_dest_path = os.path.join(temp_dir, f"temp_{job.id}.{dest_ext}")

                    await self._transcode_audio(
                        temp_raw_path, temp_dest_path, job.format, bitrate
                    )

                    if os.path.exists(temp_raw_path):
                        os.remove(temp_raw_path)

                    temp_path = temp_dest_path
                else:
                    if provider_setting == "spotiflac":
                        logger.info("Using SpotiFLAC download provider.")
                        provider = SpotiFLACProvider()
                    else:
                        logger.info("Using Deezspot download provider.")
                        provider = self.download_provider

                    loop = asyncio.get_running_loop()

                    async def provider_progress(prog_pct: float, status_str: str):
                        # Scale progress from 10% to 50%
                        scaled_prog = 10.0 + (prog_pct / 100.0) * 40.0
                        await job_queue.update_progress(
                            job.id, scaled_prog, "downloading"
                        )

                    def sync_progress(prog_pct: float, status_str: str):
                        asyncio.run_coroutine_threadsafe(
                            provider_progress(prog_pct, status_str), loop
                        )

                    temp_path = await provider.download(
                        track=track,
                        format=job.format,
                        output_dir=temp_dir,
                        filename_template="",
                        on_progress=sync_progress,
                    )

                if await self._verify(temp_path, job.format):
                    break
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                temp_path = None
            except Exception as e:
                logger.error(f"Download attempt {attempt + 1} failed: {e}")
                if temp_raw_path and os.path.exists(temp_raw_path):
                    try:
                        os.remove(temp_raw_path)
                    except Exception:
                        pass
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                temp_path = None
            await asyncio.sleep(2.0)

        if not temp_path:
            await job_queue.mark_failed(
                job.id, "Download integrity failed after 3 retries."
            )
            return

        # Lyrics
        await job_queue.update_progress(job.id, 60.0, "fetching_lyrics")
        lyrics, ltype = await self.lyrics_provider.fetch(track.title, track.artist)
        if lyrics:
            conn = await db.get_connection()
            try:
                await conn.execute(
                    "INSERT INTO lyrics_results (track_id, provider, lyrics_type, content) "
                    "VALUES (?, 'waterfall', ?, ?)",
                    (track.id, ltype, lyrics),
                )
                await conn.commit()
            finally:
                await conn.close()

        # Cover art
        await job_queue.update_progress(job.id, 75.0, "embedding_cover")
        cover = None
        if album.cover_url:
            cover = await image_cache.get_or_download(album.cover_url, "cover")
        if not cover and movie.poster_url:
            cover = await image_cache.get_or_download(movie.poster_url, "poster")
        if cover:
            try:
                await self.tagging_provider.embed_cover(temp_path, cover)
            except Exception as e:
                logger.error(f"Cover embed failed: {e}")

        # Metadata + lyrics tags
        await job_queue.update_progress(job.id, 85.0, "embedding_metadata")
        if lyrics and await settings_manager.get("embed_lyrics") == "true":
            try:
                await self.tagging_provider.embed_lyrics(
                    temp_path, lyrics, ltype == "synced"
                )
            except Exception as e:
                logger.error(f"Lyrics embed failed: {e}")
        try:
            await self.tagging_provider.embed_metadata(
                temp_path,
                track.title,
                track.artist,
                album.title,
                movie.year,
                track.track_number,
            )
        except Exception as e:
            logger.error(f"Metadata embed failed: {e}")

        # Move to destination
        await job_queue.update_progress(job.id, 95.0, "copying_to_destination")
        try:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(temp_path, abs_path)
            if lyrics and await settings_manager.get("save_lrc_file") == "true":
                ext = "lrc" if ltype == "synced" else "txt"
                with open(
                    abs_path.rsplit(".", 1)[0] + f".{ext}", "w", encoding="utf-8"
                ) as f:
                    f.write(lyrics)
            await download_cache.add(track_hash, abs_path, job.format)
            await self.folder_service.write_movie_metadata(movie, target_dir)
            await self.folder_service.generate_m3u_playlist(target_dir, album.title)
            await job_queue.mark_completed(job.id, abs_path)
        except Exception as e:
            await job_queue.mark_failed(job.id, f"Save error: {e}")

    async def _verify(self, path: str, fmt: str) -> bool:
        if not path or not os.path.exists(path):
            return False
        sz = os.path.getsize(path)
        if sz < (500 * 1024 if fmt.lower() == "mp3" else 2 * 1024 * 1024):
            return False
        if fmt.lower() == "flac":
            try:
                from mutagen.flac import FLAC

                FLAC(path)
            except Exception:
                return False
        return True

    async def _cleanup(self, job: DownloadJob) -> None:
        temp_dir = os.path.join(Path(__file__).resolve().parent.parent, "cache", "temp")
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    fp = os.path.join(temp_dir, f)
                    if os.path.isfile(fp):
                        os.remove(fp)
                except Exception:
                    pass


download_service = DownloadService()
