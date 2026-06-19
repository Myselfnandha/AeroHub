import asyncio
import logging
from typing import Optional, List, Dict
from movie_song_downloader.core.database import db
from movie_song_downloader.core.models import DownloadJob
from movie_song_downloader.core.event_bus import event_bus, Event
from movie_song_downloader.config import DOWNLOADS_LOG_PATH

downloads_logger = logging.getLogger("movie_song_downloader.Downloads")
if not downloads_logger.handlers:
    handler = logging.FileHandler(DOWNLOADS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    downloads_logger.addHandler(handler)
    downloads_logger.setLevel(logging.INFO)

_JOBS_JOIN_QUERY = """
    SELECT j.id, j.track_id, j.status, j.progress, j.output_path, j.format,
           j.error_message, j.retry_count,
           t.title, t.artist, a.title, m.title, a.cover_cached_path
    FROM download_jobs j
    JOIN tracks t ON j.track_id = t.id
    JOIN albums a ON t.album_id = a.id
    JOIN movies m ON a.movie_id = m.id
"""


def _row_to_job(row) -> DownloadJob:
    return DownloadJob(
        id=row[0],
        track_id=row[1],
        status=row[2],
        progress=row[3],
        output_path=row[4],
        format=row[5],
        error_message=row[6],
        retry_count=row[7],
        track_title=row[8],
        track_artist=row[9],
        album_title=row[10],
        movie_title=row[11],
        cover_cached_path=row[12],
    )


class JobQueue:
    def __init__(self):
        self._active_tasks: Dict[int, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def enqueue(self, track_id: int, format: str = "mp3") -> int:
        conn = await db.get_connection()
        try:
            cursor = await conn.execute(
                "INSERT INTO download_jobs (track_id, format, status, progress) VALUES (?, ?, 'queued', 0.0)",
                (track_id, format),
            )
            job_id = cursor.lastrowid
            await conn.commit()
            downloads_logger.info(
                f"Enqueued job {job_id} for track {track_id} ({format})"
            )
            async with conn.execute(
                "SELECT title FROM tracks WHERE id = ?", (track_id,)
            ) as c:
                r = await c.fetchone()
                title = r[0] if r else f"Track {track_id}"
            event_bus.publish_fire_and_forget(
                Event("job.queued", {"job_id": job_id, "track_title": title})
            )
            return job_id
        finally:
            await conn.close()

    async def dequeue(self) -> Optional[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = (
                _JOBS_JOIN_QUERY
                + " WHERE j.status = 'queued' ORDER BY j.created_at ASC LIMIT 1"
            )
            async with conn.execute(query) as cursor:
                row = await cursor.fetchone()
                return _row_to_job(row) if row else None
        finally:
            await conn.close()

    async def update_progress(self, job_id: int, progress: float, status: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=?, status=?, updated_at=datetime('now') WHERE id=?",
                (progress, status, job_id),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {
                        "job_id": job_id,
                        "progress": progress,
                        "status": status,
                    },
                )
            )
        finally:
            await conn.close()

    async def mark_completed(self, job_id: int, output_path: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET progress=100.0, status='completed', output_path=?, "
                "error_message=NULL, updated_at=datetime('now') WHERE id=?",
                (output_path, job_id),
            )
            await conn.commit()
            downloads_logger.info(f"Job {job_id} completed -> {output_path}")
            event_bus.publish_fire_and_forget(
                Event("job.completed", {"job_id": job_id, "output_path": output_path})
            )
        finally:
            await conn.close()

    async def mark_failed(self, job_id: int, error: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='failed', error_message=?, "
                "retry_count=retry_count+1, updated_at=datetime('now') WHERE id=?",
                (error, job_id),
            )
            await conn.commit()
            downloads_logger.error(f"Job {job_id} failed: {error}")
            event_bus.publish_fire_and_forget(
                Event("job.failed", {"job_id": job_id, "error": error})
            )
        finally:
            await conn.close()

    async def pause(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='paused', updated_at=datetime('now') WHERE id=? AND status='queued'",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "paused"},
                )
            )
        finally:
            await conn.close()

    async def resume(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='queued', updated_at=datetime('now') "
                "WHERE id=? AND status IN ('paused','failed','cancelled')",
                (job_id,),
            )
            await conn.commit()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "queued"},
                )
            )
        finally:
            await conn.close()

    async def cancel(self, job_id: int) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "UPDATE download_jobs SET status='cancelled', updated_at=datetime('now') WHERE id=?",
                (job_id,),
            )
            await conn.commit()
            downloads_logger.info(f"Cancelled job {job_id}")
            async with self._lock:
                task = self._active_tasks.get(job_id)
            if task and not task.done():
                task.cancel()
            event_bus.publish_fire_and_forget(
                Event(
                    "job.progress",
                    {"job_id": job_id, "progress": 0.0, "status": "cancelled"},
                )
            )
        finally:
            await conn.close()

    async def register_task(self, job_id: int, task: asyncio.Task) -> None:
        async with self._lock:
            self._active_tasks[job_id] = task

    async def unregister_task(self, job_id: int) -> None:
        async with self._lock:
            self._active_tasks.pop(job_id, None)

    async def get_all_jobs(self) -> List[DownloadJob]:
        conn = await db.get_connection()
        try:
            query = _JOBS_JOIN_QUERY + " ORDER BY j.created_at DESC"
            async with conn.execute(query) as cursor:
                return [_row_to_job(row) for row in await cursor.fetchall()]
        finally:
            await conn.close()


job_queue = JobQueue()
