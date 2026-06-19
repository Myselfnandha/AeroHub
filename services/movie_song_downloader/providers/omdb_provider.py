import time
import httpx
import logging
import hashlib
from typing import List, Optional

from movie_song_downloader.core.models import Movie
from movie_song_downloader.core.settings_manager import settings_manager
from movie_song_downloader.core.rate_limiter import rate_limiter, providers_logger
from movie_song_downloader.core.cache_manager import api_cache
from movie_song_downloader.config import OMDB_BASE_URL

logger = logging.getLogger("movie_song_downloader.OMDbProvider")


class OMDbProvider:
    """Optional fallback provider for movie ratings, cast, and plot via OMDb API."""

    async def _request(self, params: dict, cache_ttl: int = 2592000) -> Optional[dict]:
        """Make OMDb API request with caching. TTL default 30 days."""
        api_key = await settings_manager.get("omdb_api_key")
        if not api_key:
            logger.debug("OMDb API key not configured.")
            return None

        full_params = {**params, "apikey": api_key}
        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"omdb:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("omdb")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(OMDB_BASE_URL, params=full_params)
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("Response") == "True":
                        providers_logger.info(
                            f"provider=omdb latency={ms}ms success=True"
                        )
                        await api_cache.set(cache_key, "omdb", data, cache_ttl)
                        return data
                    providers_logger.warning(
                        f'provider=omdb latency={ms}ms response=False error="{data.get("Error")}"'
                    )
                else:
                    providers_logger.error(
                        f"provider=omdb latency={ms}ms success=False status={resp.status_code}"
                    )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=omdb latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"OMDb request failed: {e}")
        return None

    async def search(self, query: str, year: Optional[int] = None) -> List[Movie]:
        """Search OMDb for movies."""
        params = {"s": query, "type": "movie"}
        if year:
            params["y"] = str(year)

        data = await self._request(params, cache_ttl=86400)
        if not data or "Search" not in data:
            return []

        movies = []
        for item in data["Search"]:
            yr = None
            try:
                yr = int(item.get("Year", "0").split("–")[0])
            except (ValueError, IndexError):
                pass

            movies.append(
                Movie(
                    source="omdb",
                    source_id=item.get("imdbID", ""),
                    title=item.get("Title", ""),
                    year=yr,
                    poster_url=item.get("Poster")
                    if item.get("Poster") != "N/A"
                    else None,
                )
            )
        return movies

    async def get_details(self, imdb_id: str) -> Optional[dict]:
        """Fetch full movie details from OMDb by IMDb ID."""
        params = {"i": imdb_id, "plot": "short"}
        return await self._request(params, cache_ttl=2592000)

    async def enrich_movie(self, movie: Movie) -> Movie:
        """Enrich a Movie object with OMDb data (rating, cast, poster, overview).
        Tries by title+year if no imdb_id available."""
        data = None

        # If we have an IMDb ID, use it directly
        if movie.source == "omdb" and movie.source_id:
            data = await self.get_details(movie.source_id)

        # Otherwise search by title
        if not data:
            params = {"t": movie.title, "type": "movie"}
            if movie.year:
                params["y"] = str(movie.year)
            data = await self._request(params, cache_ttl=2592000)

        if not data:
            return movie

        # Enrich fields
        if not movie.poster_url or movie.poster_url == "N/A":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                movie.poster_url = poster

        movie.rating = data.get("imdbRating")
        movie.cast_info = data.get("Actors")

        if not movie.overview:
            movie.overview = data.get("Plot")

        if not movie.genres:
            genres_str = data.get("Genre", "")
            if genres_str and genres_str != "N/A":
                movie.genres = [g.strip() for g in genres_str.split(",")]

        if not movie.language:
            movie.language = data.get("Language")

        # Store IMDb ID for future lookups
        if data.get("imdbID") and not movie.source_id:
            movie.source_id = data["imdbID"]

        return movie
