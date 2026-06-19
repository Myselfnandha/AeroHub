import logging
import httpx
import hashlib
import time
from typing import List, Dict, Optional
from movie_song_downloader.core.rate_limiter import rate_limiter, providers_logger
from movie_song_downloader.core.cache_manager import api_cache

logger = logging.getLogger("movie_song_downloader.WikidataProvider")

USER_AGENT = "movie_song_downloader/2.0 (contact: nandha.dev@gmail.com)"


class WikidataProvider:
    async def _wikidata_request(
        self, params: dict, cache_ttl: int = 604800
    ) -> Optional[dict]:
        """Make a request to Wikidata API with caching and rate limiting."""
        params["format"] = "json"
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"wikidata:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("wikidata")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    "https://www.wikidata.org/w/api.php",
                    params=params,
                    headers={"User-Agent": USER_AGENT},
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=wikidata latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, "wikidata", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=wikidata latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=wikidata latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"Wikidata API request failed: {e}")
        return None

    async def get_posters_batch(
        self, wikipedia_titles: List[str], lang: str = "en"
    ) -> Dict[str, str]:
        """
        Query Wikidata API in batches to resolve P18 (image) property for Wikipedia page titles.
        Returns a dictionary mapping {wikipedia_title: poster_url}.
        """
        if not wikipedia_titles:
            return {}

        results = {}
        site = "enwiki" if lang == "en" else "tawiki"

        # Wikipedia allows batching up to 50 items
        batch_size = 40
        for i in range(0, len(wikipedia_titles), batch_size):
            batch = wikipedia_titles[i:i+batch_size]
            params = {
                "action": "wbgetentities",
                "sites": site,
                "titles": "|".join(batch),
                "props": "claims|sitelinks",
            }

            data = await self._wikidata_request(params, cache_ttl=86400 * 7)
            if not data or "entities" not in data:
                continue

            entities = data["entities"]
            for entity_id, entity_data in entities.items():
                if entity_id == "-1":
                    continue

                # Retrieve the original title from sitelinks to map correctly
                sitelinks = entity_data.get("sitelinks", {})
                wiki_site = sitelinks.get(site, {})
                title = wiki_site.get("title")
                if not title:
                    continue

                claims = entity_data.get("claims", {})
                p18_claims = claims.get("P18", [])
                if p18_claims:
                    # Get filename from the claim
                    mainsnak = p18_claims[0].get("mainsnak", {})
                    datavalue = mainsnak.get("datavalue", {})
                    filename = datavalue.get("value")
                    if filename:
                        # Construct Wikimedia Commons Special:FilePath URL
                        # Special:FilePath redirects directly to the raw media URL
                        url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}"
                        results[title] = url

        return results
