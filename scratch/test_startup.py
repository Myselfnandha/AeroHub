import asyncio
import sys
import logging

logging.basicConfig(level=logging.INFO)

async def test():
    print("Setting up paths...", flush=True)
    sys.path.insert(0, "c:/Users/NANDHA A/Desktop/UTILITIES")
    
    print("Importing app...", flush=True)
    from MovieSongDownloader.MovieSongDownloader import startup_event
    
    print("Running startup_event() with 10s timeout...", flush=True)
    try:
        await asyncio.wait_for(startup_event(), timeout=10.0)
        print("Startup event completed successfully!", flush=True)
    except asyncio.TimeoutError:
        print("Timeout! Startup event hung!", flush=True)
    except Exception as e:
        print(f"Error occurred: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test())
