import asyncio
import re
import logging
import time
import json
from typing import Tuple, Optional
import syncedlyrics
from movie_song_downloader.providers.base import BaseLyricsProvider
from movie_song_downloader.core.settings_manager import settings_manager
from movie_song_downloader.core.rate_limiter import rate_limiter, providers_logger

logger = logging.getLogger("movie_song_downloader.LyricsProvider")


class LyricsProvider(BaseLyricsProvider):
    def __init__(self):
        self._lrc_re = re.compile(r"\[\d{2,}:\d{2}(?:\.\d{1,3})?\]")

    def _is_synced(self, text: str) -> bool:
        return bool(text) and len(self._lrc_re.findall(text)) >= 3

    @staticmethod
    def _search(query: str, provider: str) -> Optional[str]:
        try:
            return syncedlyrics.search(query, providers=[provider])
        except Exception:
            return None

    async def fetch(self, title: str, artist: str) -> Tuple[Optional[str], str]:
        raw = await settings_manager.get("lyrics_priority")
        try:
            providers = json.loads(raw)
        except Exception:
            providers = ["lrclib", "syncedlyrics", "musixmatch", "genius"]

        query = f"{title} {artist}"
        for prov in providers:
            await rate_limiter.acquire("lyrics")
            t0 = time.time()
            try:
                target = prov.lower()
                if target == "syncedlyrics":
                    result = await asyncio.to_thread(syncedlyrics.search, query)
                else:
                    result = await asyncio.to_thread(self._search, query, target)
                ms = int((time.time() - t0) * 1000)
                if result:
                    providers_logger.info(
                        f"provider=lyrics_{prov} latency={ms}ms success=True response_size={len(result)}"
                    )
                    ltype = "synced" if self._is_synced(result) else "plain"
                    return result, ltype
                providers_logger.info(
                    f"provider=lyrics_{prov} latency={ms}ms success=False response_size=0"
                )
            except Exception as e:
                ms = int((time.time() - t0) * 1000)
                providers_logger.error(
                    f'provider=lyrics_{prov} latency={ms}ms success=False error="{e}"'
                )
        return None, "none"
