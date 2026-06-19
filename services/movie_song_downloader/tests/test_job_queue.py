import pytest
from movie_song_downloader.core.database import db
from movie_song_downloader.core.job_queue import job_queue


@pytest.mark.asyncio
async def test_job_queue_state_transitions():
    await db.run_migrations()

    conn = await db.get_connection()
    try:
        # Seed a dummy movie, album, and track to satisfy foreign keys
        await conn.execute(
            (
                "INSERT OR REPLACE INTO movies (id, tmdb_id, title) "
                "VALUES (99, 999, 'Test Movie')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO albums (id, movie_id, spotify_id, title) "
                "VALUES (99, 99, 'album_99', 'Test Album')"
            )
        )
        await conn.execute(
            (
                "INSERT OR REPLACE INTO tracks (id, album_id, spotify_id, title, track_number) "
                "VALUES (99, 99, 'track_99', 'Test Track', 1)"
            )
        )
        await conn.commit()
    finally:
        await conn.close()

    # Enqueue a job
    job_id = await job_queue.enqueue(track_id=99, format="mp3")
    assert job_id > 0

    # Dequeue the job
    job = await job_queue.dequeue()
    assert job is not None
    assert job.id == job_id
    assert job.status == "queued"

    # Update progress
    await job_queue.update_progress(job_id, 45.0, "downloading")

    # Verify status changed
    jobs = await job_queue.get_all_jobs()
    active_job = [j for j in jobs if j.id == job_id][0]
    assert active_job.status == "downloading"
    assert active_job.progress == 45.0

    # Cancel job
    await job_queue.cancel(job_id)

    # Verify status is cancelled
    jobs = await job_queue.get_all_jobs()
    cancelled_job = [j for j in jobs if j.id == job_id][0]
    assert cancelled_job.status == "cancelled"
