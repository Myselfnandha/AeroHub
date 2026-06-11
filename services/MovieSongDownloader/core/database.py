import re
import aiosqlite
import logging
from pathlib import Path
from MovieSongDownloader.config import DATABASE_PATH

logger = logging.getLogger("MovieSongDownloader.Database")


class DatabaseManager:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path

    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL;")
        await conn.execute("PRAGMA synchronous=NORMAL;")
        await conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    async def run_migrations(self, max_version: int = 99) -> None:
        migrations_dir = Path(__file__).resolve().parent / "migrations"
        if not migrations_dir.exists():
            logger.warning("Migrations directory not found, skipping.")
            return

        conn = await self.get_connection()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT DEFAULT (datetime('now'))
                );
            """)
            await conn.commit()

            async with conn.execute("SELECT version FROM schema_migrations") as cursor:
                applied_versions = {row[0] for row in await cursor.fetchall()}

            migration_files = []
            for filepath in migrations_dir.glob("*.sql"):
                match = re.match(r"^(\d+)_(.+)\.sql$", filepath.name)
                if match:
                    version = int(match.group(1))
                    migration_files.append((version, filepath))

            migration_files.sort(key=lambda x: x[0])

            for version, filepath in migration_files:
                if version > max_version:
                    continue
                if version not in applied_versions:
                    logger.info(f"Applying migration v{version}: {filepath.name}")
                    try:
                        sql_content = filepath.read_text(encoding="utf-8")
                        await conn.executescript(sql_content)
                        await conn.execute(
                            "INSERT INTO schema_migrations (version) VALUES (?)",
                            (version,),
                        )
                        await conn.commit()
                        logger.info(f"Migration v{version} applied.")
                    except Exception as e:
                        await conn.rollback()
                        logger.error(f"Migration {filepath.name} failed: {e}")
                        raise
        finally:
            await conn.close()


db = DatabaseManager()
