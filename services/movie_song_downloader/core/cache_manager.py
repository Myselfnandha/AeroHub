import os
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
import httpx
from movie_song_downloader.config import POSTERS_CACHE_DIR, COVERS_CACHE_DIR
from movie_song_downloader.core.database import db

logger = logging.getLogger("movie_song_downloader.CacheManager")


class DownloadCache:
    @staticmethod
    def generate_hash(artist: str, title: str, album: str, duration_ms: int) -> str:
        raw = f"{artist.lower()}|{title.lower()}|{album.lower()}|{duration_ms}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def check(self, track_hash: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT file_path, format, downloaded_at FROM download_cache WHERE track_hash = ?",
                (track_hash,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if os.path.exists(row[0]):
                        return {
                            "file_path": row[0],
                            "format": row[1],
                            "downloaded_at": row[2],
                        }
                    await conn.execute(
                        "DELETE FROM download_cache WHERE track_hash = ?", (track_hash,)
                    )
                    await conn.commit()
                    logger.warning(f"Pruned stale cache entry: {track_hash}")
            return None
        finally:
            await conn.close()

    async def add(self, track_hash: str, file_path: str, fmt: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO download_cache (track_hash, file_path, format) VALUES (?, ?, ?)",
                (track_hash, file_path, fmt),
            )
            await conn.commit()
        finally:
            await conn.close()


class ImageCache:
    def __init__(self):
        self.poster_dir = POSTERS_CACHE_DIR
        self.cover_dir = COVERS_CACHE_DIR

    async def get_or_download(self, url: str, category: str) -> Optional[str]:
        if not url:
            return None
        target_dir = self.poster_dir if category == "poster" else self.cover_dir
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        ext = "png"
        clean_url = url.split("?")[0]
        if "." in clean_url:
            potential = clean_url.rsplit(".", 1)[-1].lower()
            if potential in ("jpg", "jpeg", "png", "webp"):
                ext = potential
        local_path = target_dir / f"{url_hash}.{ext}"
        if local_path.exists():
            return str(local_path)
        headers = {
            "User-Agent": "movie_song_downloader/2.0 (contact: nandha.dev@gmail.com)"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(resp.content)
                    return str(local_path)
                logger.warning(f"Image download HTTP {resp.status_code}: {url}")
        except Exception as e:
            logger.error(f"Image download failed: {e}")
        return None


class APICache:
    async def get(self, cache_key: str) -> Optional[dict]:
        conn = await db.get_connection()
        try:
            async with conn.execute(
                "SELECT json_payload, expires_at FROM api_cache WHERE cache_key = ?",
                (cache_key,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    if datetime.now() < datetime.fromisoformat(row[1]):
                        try:
                            return json.loads(row[0])
                        except json.JSONDecodeError:
                            logger.error(f"Corrupt cache key: {cache_key}")
                    else:
                        await conn.execute(
                            "DELETE FROM api_cache WHERE cache_key = ?", (cache_key,)
                        )
                        await conn.commit()
            return None
        finally:
            await conn.close()

    async def set(
        self,
        cache_key: str,
        provider: str,
        payload: dict,
        ttl: int = 86400,
        expires_in_seconds: Optional[int] = None,
    ) -> None:
        if expires_in_seconds is not None:
            ttl = expires_in_seconds
        conn = await db.get_connection()
        try:
            expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
            await conn.execute(
                "INSERT OR REPLACE INTO api_cache (cache_key, provider, json_payload, expires_at) VALUES (?, ?, ?, ?)",
                (cache_key, provider, json.dumps(payload), expires_at),
            )
            await conn.commit()
        finally:
            await conn.close()

    async def verify_scraped_data(
        self, cache_key: str, new_data: dict, fields: list
    ) -> dict:
        """Compare freshly scraped data against cached version.
        Returns merged result preferring cached values for stable fields (IDs)
        and new values for volatile fields (ratings, availability)."""
        cached = await self.get(cache_key)
        if cached is None:
            return new_data

        merged = {**cached}
        for field in fields:
            if field in new_data:
                merged[field] = new_data[field]
        return merged


download_cache = DownloadCache()
image_cache = ImageCache()
api_cache = APICache()
