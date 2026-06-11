import json
import logging
from pathlib import Path
from MovieSongDownloader.config import SETTINGS_BACKUP_PATH, DEFAULT_SETTINGS
from MovieSongDownloader.core.database import db

logger = logging.getLogger("MovieSongDownloader.SettingsManager")

CATEGORY_MAP = {
    "tmdb_api_key": "api",
    "tmdb_base_url": "api",
    "spotify_client_id": "api",
    "spotify_client_secret": "api",
    "deezer_arl": "api",
    "audio_format": "download",
    "bitrate": "download",
    "output_dir": "download",
    "filename_format": "download",
    "folder_format": "download",
    "download_mode": "download",
    "max_concurrent": "download",
    "lyrics_priority": "lyrics",
    "save_lrc_file": "lyrics",
    "embed_lyrics": "lyrics",
    "theme": "ui",
    "default_tab": "ui",
    "language_region": "ui",
    "check_interval_hours": "watchlist",
    "auto_download": "watchlist",
    "notify_on_found": "watchlist",
    "last_fetch_date": "watchlist",
    "doh_enabled": "network",
    "dns_provider": "network",
}


def _get_category(key: str) -> str:
    return CATEGORY_MAP.get(key, "ui")


class SettingsManager:
    def __init__(self, backup_path: Path = SETTINGS_BACKUP_PATH):
        self.backup_path = backup_path

    async def get_all(self) -> dict:
        conn = await db.get_connection()
        try:
            async with conn.execute("SELECT key, value FROM settings") as cursor:
                rows = await cursor.fetchall()
            if not rows:
                logger.warning("Settings empty. Attempting backup restore...")
                restored = await self.restore_from_backup()
                if not restored:
                    logger.info("Seeding defaults...")
                    await self._seed_defaults(conn)
                    restored = DEFAULT_SETTINGS.copy()
                else:
                    await self._save_many_to_conn(conn, restored)
                return restored
            return {row[0]: row[1] for row in rows}
        finally:
            await conn.close()

    async def get(self, key: str) -> str:
        all_s = await self.get_all()
        return all_s.get(key, DEFAULT_SETTINGS.get(key, ""))

    async def set(self, key: str, value: str) -> None:
        conn = await db.get_connection()
        try:
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (key, str(value), _get_category(key)),
            )
            await conn.commit()
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def save_many(self, settings_dict: dict) -> None:
        conn = await db.get_connection()
        try:
            await self._save_many_to_conn(conn, settings_dict)
            updated = await self.get_all()
            await self.export_backup(updated)
        finally:
            await conn.close()

    async def _save_many_to_conn(self, conn, data: dict) -> None:
        for k, v in data.items():
            await conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, category) VALUES (?, ?, ?)",
                (k, str(v), _get_category(k)),
            )
        await conn.commit()

    async def _seed_defaults(self, conn) -> None:
        await self._save_many_to_conn(conn, DEFAULT_SETTINGS)
        await self.export_backup(DEFAULT_SETTINGS)

    async def export_backup(self, data: dict) -> None:
        try:
            with open(self.backup_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Backup export failed: {e}")

    async def restore_from_backup(self) -> dict:
        if not self.backup_path.exists():
            return {}
        try:
            with open(self.backup_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Backup restore failed: {e}")
            return {}


settings_manager = SettingsManager()
