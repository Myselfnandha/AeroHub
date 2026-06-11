import os
import sys
import httpx
import logging
import asyncio
from typing import Optional, Callable

if "youtube_dl" not in sys.modules:
    import yt_dlp

    sys.modules["youtube_dl"] = yt_dlp

bin_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin"
)
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

import deezload.base  # noqa: E402

if not getattr(deezload.base.extract_video_id, "__patched__", False):
    _orig = deezload.base.extract_video_id

    def _patched(qs: str):
        try:
            qs = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            pass
        qs = qs.replace(r"\u0026", "&").replace("\\u0026", "&")
        return _orig(qs)

    _patched.__patched__ = True
    deezload.base.extract_video_id = _patched

from MovieSongDownloader.providers.base import BaseDownloadProvider  # noqa: E402
from MovieSongDownloader.core.models import Track  # noqa: E402
from MovieSongDownloader.core.rate_limiter import rate_limiter  # noqa: E402

logger = logging.getLogger("MovieSongDownloader.DeezspotProvider")


class DeezspotProvider(BaseDownloadProvider):
    async def _resolve_deezer_id(self, title: str, artist: str) -> Optional[int]:
        await rate_limiter.acquire("lyrics")
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        url = "https://api.deezer.com/search"

        for params in [
            {"q": f'track:"{clean_title}" artist:"{clean_artist}"'},
            {"q": f"{clean_artist} {clean_title}"},
        ]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("data"):
                            return data["data"][0]["id"]
            except Exception as e:
                logger.error(f"Deezer search error: {e}")
        return None

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        deezer_id = await self._resolve_deezer_id(track.title, track.artist)
        if not deezer_id:
            raise Exception(
                f"Could not resolve '{track.title}' by '{track.artist}' on Deezer."
            )

        deezer_url = f"https://www.deezer.com/track/{deezer_id}"
        await rate_limiter.acquire("deezspot")
        logger.info(f"Downloading Deezer ID {deezer_id} ({format})...")

        def _task():
            from deezload.base import Loader, LoadStatus

            loader = Loader(
                urls=[deezer_url],
                output_dir=output_dir,
                format=format.lower(),
                tree=False,
                slugify=False,
            )
            path = None
            ok = False
            err = None
            for status, t, i, prog in loader.load_gen():
                if on_progress:
                    on_progress(
                        float(int(prog * 100)), f"deezload_{status.name.lower()}"
                    )
                if status in (LoadStatus.FINISHED, LoadStatus.SKIPPED):
                    path = t.path
                    ok = True
                elif status == LoadStatus.FAILED:
                    err = "Track not found on YouTube."
                elif status == LoadStatus.ERROR:
                    err = "deezload internal error."
            if not ok:
                raise Exception(err or "Download failed.")
            return path

        loop = asyncio.get_running_loop()
        local_path = await loop.run_in_executor(None, _task)
        if not local_path or not os.path.exists(local_path):
            raise FileNotFoundError(f"File not found after download: {local_path}")
        logger.info(f"Downloaded -> {local_path}")
        return local_path
