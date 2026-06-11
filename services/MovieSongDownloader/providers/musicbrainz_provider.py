import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional, Tuple
from MovieSongDownloader.core.rate_limiter import rate_limiter, providers_logger
from MovieSongDownloader.core.cache_manager import api_cache
from MovieSongDownloader.core.models import Album, Track

logger = logging.getLogger("MovieSongDownloader.MusicBrainzProvider")

USER_AGENT = "MovieSongDownloader/2.0 (contact: nandha.dev@gmail.com)"


class MusicBrainzProvider:
    async def _mb_request(
        self, url: str, params: dict, cache_ttl: int = 2592000
    ) -> Optional[dict]:
        """Make a request to MusicBrainz API with caching and strict 1 req/sec rate limit."""
        params["fmt"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"musicbrainz:{hashlib.md5((url + param_str).encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        # MusicBrainz guidelines mandate strict rate limits (1 req/sec)
        await rate_limiter.acquire("musicbrainz")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    url, params=params, headers={"User-Agent": USER_AGENT}
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=musicbrainz latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "musicbrainz", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=musicbrainz latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=musicbrainz latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"MusicBrainz API request failed: {e}")
        return None

    async def enrich_album(
        self, album: Album, tracks: List[Track]
    ) -> Tuple[Optional[str], Dict[str, str]]:
        """
        Enrich Album with composer info and Tracks with ISRC codes from MusicBrainz.
        Returns: (composer_name, {track_title: isrc_code})
        """
        composer = None
        isrc_map = {}

        # 1. Search release groups
        query = f'release-group:"{album.title}" AND type:soundtrack'
        if album.artist and album.artist != "Unknown":
            # Add artist if known to narrow down
            query += f' AND artist:"{album.artist}"'

        search_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release-group/", {"query": query}
        )

        if not search_data or not search_data.get("release-groups"):
            # Try a broader search without soundtrack filter
            query_broad = f'release-group:"{album.title}"'
            search_data = await self._mb_request(
                "https://musicbrainz.org/ws/2/release-group/", {"query": query_broad}
            )
            if not search_data or not search_data.get("release-groups"):
                return None, {}

        rg = search_data["release-groups"][0]
        rg_id = rg["id"]

        # If artist-credit lists the composer, capture it
        artist_credit = rg.get("artist-credit", [])
        if artist_credit:
            composer = artist_credit[0].get("artist", {}).get("name")

        # 2. Browse releases for this release group to find tracks/recordings and relations
        browse_data = await self._mb_request(
            "https://musicbrainz.org/ws/2/release",
            {
                "release-group": rg_id,
                "inc": "recordings+artist-rels+work-rels+isrcs+work-level-rels",
            },
        )

        if not browse_data or not browse_data.get("releases"):
            return composer, {}

        # Look through releases
        for rel in browse_data["releases"]:
            # Check release relations for composer if not resolved
            if not composer:
                for rel_item in rel.get("relations", []):
                    if rel_item.get("type") == "composer" and rel_item.get("artist"):
                        composer = rel_item["artist"].get("name")
                        break

            # Collect recordings and ISRCs
            media_list = rel.get("media", [])
            for media in media_list:
                for mb_track in media.get("tracks", []):
                    title = mb_track.get("title", "")
                    recording = mb_track.get("recording", {})
                    isrcs = recording.get("isrcs", [])

                    if isrcs:
                        isrc_map[title.lower().strip()] = isrcs[0]

                    # Check recording level relations for composer if still not found
                    if not composer:
                        for rec_rel in recording.get("relations", []):
                            if rec_rel.get("type") == "composer" and rec_rel.get(
                                "artist"
                            ):
                                composer = rec_rel["artist"].get("name")
                                break

        # Match ISRCs back to JioSaavn tracks by title matching
        final_isrcs = {}
        for t in tracks:
            t_title_clean = t.title.lower().strip()
            # Try exact match first
            if t_title_clean in isrc_map:
                final_isrcs[t.title] = isrc_map[t_title_clean]
            else:
                # Try partial match (e.g. "Song Name (From film)" vs "Song Name")
                matched = False
                for mb_title, isrc in isrc_map.items():
                    if mb_title in t_title_clean or t_title_clean in mb_title:
                        final_isrcs[t.title] = isrc
                        matched = True
                        break
                if not matched:
                    # Try cleaning common suffixes
                    clean_jio = t_title_clean.split("(")[0].strip()
                    for mb_title, isrc in isrc_map.items():
                        clean_mb = mb_title.split("(")[0].strip()
                        if clean_jio == clean_mb:
                            final_isrcs[t.title] = isrc
                            break

        return composer, final_isrcs
