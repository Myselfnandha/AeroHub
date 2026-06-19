import asyncio
import time
import logging
from movie_song_downloader.config import PROVIDERS_LOG_PATH

providers_logger = logging.getLogger("movie_song_downloader.Providers")
if not providers_logger.handlers:
    handler = logging.FileHandler(PROVIDERS_LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    providers_logger.addHandler(handler)
    providers_logger.setLevel(logging.INFO)


class RateLimiter:
    def __init__(self, rps: float, name: str):
        self.delay = 1.0 / rps if rps > 0 else 0.0
        self.last_called = 0.0
        self.name = name
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        if self.delay <= 0:
            return
        async with self._lock:
            now = time.time()
            wait = self.delay - (now - self.last_called)
            if wait > 0:
                providers_logger.debug(
                    f"provider={self.name} rate_limit sleep_ms={int(wait * 1000)}"
                )
                await asyncio.sleep(wait)
            self.last_called = time.time()


class GlobalRateLimiters:
    def __init__(self):
        self._limiters = {
            "wikipedia": RateLimiter(5.0, "wikipedia"),
            "jiosaavn": RateLimiter(2.0, "jiosaavn"),
            "omdb": RateLimiter(3.0, "omdb"),
            "lyrics": RateLimiter(2.0, "lyrics"),
            "deezspot": RateLimiter(1.0, "deezspot"),
        }
        self._lock = asyncio.Lock()

    async def acquire(self, provider: str) -> None:
        key = provider.lower()
        async with self._lock:
            if key not in self._limiters:
                self._limiters[key] = RateLimiter(2.0, key)
            limiter = self._limiters[key]
        await limiter.acquire()


rate_limiter = GlobalRateLimiters()
