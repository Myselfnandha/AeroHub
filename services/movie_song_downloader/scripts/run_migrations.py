import asyncio
import traceback

from MovieSongDownloader.core.database import db

async def main():
    try:
        print('Running migrations...', flush=True)
        await db.run_migrations()
        print('Migrations applied successfully', flush=True)
    except Exception as e:
        print('Migration failed:', e)
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
