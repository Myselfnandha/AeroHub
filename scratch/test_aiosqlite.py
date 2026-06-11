import asyncio
import aiosqlite
from pathlib import Path

async def test():
    db_path = Path(r"c:\Users\NANDHA A\Desktop\UTILITIES\MovieSongDownloader\db.sqlite3")
    print(f"Connecting to database at {db_path}...", flush=True)
    try:
        conn = await asyncio.wait_for(aiosqlite.connect(db_path), timeout=5.0)
        print("Connected! Running PRAGMA...", flush=True)
        await asyncio.wait_for(conn.execute("PRAGMA journal_mode=WAL;"), timeout=5.0)
        print("PRAGMA WAL set! Querying schema_migrations...", flush=True)
        async with conn.execute("SELECT version FROM schema_migrations") as cursor:
            rows = await asyncio.wait_for(cursor.fetchall(), timeout=5.0)
            print(f"Success! Rows: {rows}", flush=True)
        await conn.close()
    except Exception as e:
        print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
