import time
import httpx
import logging
import hashlib
import re
import datetime
from typing import List, Optional
from scrapling import Selector, AsyncFetcher
import asyncio

from movie_song_downloader.providers.base import BaseMovieProvider
from movie_song_downloader.core.models import Movie
from movie_song_downloader.core.rate_limiter import rate_limiter, providers_logger
from movie_song_downloader.core.cache_manager import api_cache
from movie_song_downloader.config import WIKIPEDIA_EN_API, WIKIPEDIA_TA_API

logger = logging.getLogger("movie_song_downloader.WikipediaProvider")

USER_AGENT = "movie_song_downloader/2.0 (contact: nandha.dev@gmail.com)"


class WikipediaProvider(BaseMovieProvider):
    async def _wiki_request(
        self, params: dict, lang: str = "en", cache_ttl: int = 604800
    ) -> Optional[dict]:
        """Make a request to Wikipedia API with caching."""
        api_url = WIKIPEDIA_EN_API if lang == "en" else WIKIPEDIA_TA_API
        params["format"] = "json"
        params["origin"] = "*"

        param_str = "".join(f"{k}={params[k]}" for k in sorted(params))
        cache_key = f"wiki_{lang}:{hashlib.md5(param_str.encode()).hexdigest()}"

        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("wikipedia")
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    api_url, params=params, headers={"User-Agent": USER_AGENT}
                )
                ms = int((time.time() - t0) * 1000)
                if resp.status_code == 200:
                    data = resp.json()
                    providers_logger.info(
                        f"provider=wikipedia_{lang} latency={ms}ms success=True"
                    )
                    await api_cache.set(cache_key, f"wikipedia_{lang}", data, cache_ttl)
                    return data
                providers_logger.error(
                    f"provider=wikipedia_{lang} latency={ms}ms success=False status={resp.status_code}"
                )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=wikipedia_{lang} latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"Wikipedia request failed: {e}")
        return None

    async def search(self, query: str, **filters) -> List[Movie]:
        """Search Wikipedia for movie pages across English and Tamil."""
        year = filters.get("year")
        search_query = f"{query} film"
        if year:
            search_query = f"{query} {year} film"

        movies = []
        seen_titles = set()

        # Search English Wikipedia
        en_results = await self._search_wiki(search_query, lang="en")
        for m in en_results:
            key = m.title.lower()
            if key not in seen_titles:
                seen_titles.add(key)
                movies.append(m)

        # Search Tamil Wikipedia for better regional coverage
        ta_results = await self._search_wiki(query, lang="ta")
        for m in ta_results:
            key = m.title.lower()
            if key not in seen_titles:
                seen_titles.add(key)
                movies.append(m)

        return movies[:20]

    async def _search_wiki(self, query: str, lang: str = "en") -> List[Movie]:
        """Search a specific Wikipedia language edition."""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": "10",
            "srprop": "snippet",
        }
        data = await self._wiki_request(params, lang=lang, cache_ttl=86400)
        if not data or "query" not in data:
            return []

        movies = []
        for item in data["query"].get("search", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            page_id = str(item.get("pageid", ""))

            # Filter: only keep film-related pages
            if not self._is_film_page(title, snippet):
                continue

            # Extract year from title pattern like "Vikram (2022 film)"
            clean_title, year = self._parse_film_title(title)

            movies.append(
                Movie(
                    source="wikipedia",
                    source_id=page_id,
                    title=clean_title,
                    year=year,
                    language="ta" if lang == "ta" else None,
                    overview=Selector(snippet).get_all_text(separator="", strip=True)[:200]
                    if snippet
                    else None,
                )
            )
        return movies

    async def get_today_releases(self, region: str = "IN") -> List[Movie]:
        """Get recent Tamil film releases from Wikipedia list pages."""
        import datetime

        current_year = datetime.datetime.now().year

        movies = []
        # Try scraping "List of Tamil films of {year}" page
        page_title = f"List of Tamil films of {current_year}"
        details = await self._get_page_html(page_title, lang="en")
        if details:
            parsed_entries = self._parse_film_list_page(details)
            if parsed_entries:
                today = datetime.date.today()
                # Start and End of the current week (Monday to Sunday)
                start_of_week = today - datetime.timedelta(days=today.weekday())
                end_of_week = start_of_week + datetime.timedelta(days=6)

                # Keep only releases <= end_of_week (excluding future movies)
                valid_entries = []
                for m, rel_date in parsed_entries:
                    if rel_date and rel_date <= end_of_week:
                        m.release_date = rel_date.isoformat()
                        valid_entries.append((m, rel_date))
                    elif not rel_date:
                        # Keep entries without valid dates at the very bottom
                        m.release_date = datetime.date(current_year, 1, 1).isoformat()
                        valid_entries.append((m, datetime.date(current_year, 1, 1)))

                # Sort by release date descending
                valid_entries.sort(key=lambda x: x[1], reverse=True)
                movies = [m for m, _ in valid_entries]

        if not movies:
            # Fallback: search for recent Tamil films
            params = {
                "action": "query",
                "list": "search",
                "srsearch": f"Tamil film {current_year}",
                "srlimit": "80",
                "srprop": "snippet",
            }
            data = await self._wiki_request(params, lang="en", cache_ttl=14400)
            if data and "query" in data:
                for item in data["query"].get("search", []):
                    title = item.get("title", "")
                    if self._is_film_page(title, item.get("snippet", "")):
                        clean_title, year = self._parse_film_title(title)
                        m = Movie(
                            source="wikipedia",
                            source_id=str(item.get("pageid", "")),
                            title=clean_title,
                            year=year or current_year,
                            language="ta",
                        )
                        m.release_date = datetime.date(current_year, 1, 1).isoformat()
                        movies.append(m)

        # Batch resolve all overviews, numeric IDs and posters (including fair-use fallback)
        if movies:
            await self._resolve_movie_details_batch(movies)

        return movies

    async def _resolve_movie_details_batch(self, movies: List[Movie]) -> List[Movie]:
        """Resolves Wikipedia poster URLs and overviews in batch by scraping each page."""
        if not movies:
            return movies

        valid_movies = [m for m in movies if m.source_id]
        if not valid_movies:
            return movies

        # Use a semaphore to limit concurrent requests
        sem = asyncio.Semaphore(5)

        async def resolve_one(m: Movie):
            async with sem:
                try:
                    details = await self.get_movie_details(m.source_id)
                    if details:
                        m.overview = details.overview
                        m.poster_url = details.poster_url
                        m.title = details.title
                        if details.year:
                            m.year = details.year
                        # Also update the source_id if it got resolved to numeric ID
                        if details.source_id:
                            m.source_id = details.source_id
                except Exception as e:
                    logger.error(f"Failed to resolve movie details for {m.title}: {e}")

        await asyncio.gather(*(resolve_one(m) for m in valid_movies), return_exceptions=True)

        # Call Wikidata fallback for any movies still missing posters
        missing_poster_movies = [m for m in valid_movies if not m.poster_url]
        if missing_poster_movies:
            try:
                from movie_song_downloader.providers.wikidata_provider import (
                    WikidataProvider,
                )

                wikidata = WikidataProvider()
                wiki_titles = [
                    m.source_id
                    for m in missing_poster_movies
                    if not m.source_id.isdigit()
                ]
                if wiki_titles:
                    wikidata_posters = await wikidata.get_posters_batch(wiki_titles)
                    for m in missing_poster_movies:
                        if m.source_id in wikidata_posters:
                            m.poster_url = wikidata_posters[m.source_id]
                            logger.info(
                                f"Resolved poster via Wikidata for: {m.title} -> {m.poster_url}"
                            )
            except Exception as e:
                logger.error(f"Wikidata poster resolution failed: {e}")

        return movies

    async def get_watch_providers(
        self, source_id: str, region: str = "IN"
    ) -> List[dict]:
        """Extract OTT platform info from Wikipedia infobox."""
        html = await self._get_page_html_by_id(source_id)
        if not html:
            return []

        text = Selector(html).get_all_text().lower()
        providers = []
        ott_map = {
            "netflix": {"id": 1, "name": "Netflix"},
            "amazon prime": {"id": 2, "name": "Amazon Prime"},
            "prime video": {"id": 2, "name": "Amazon Prime"},
            "disney+": {"id": 3, "name": "Disney+ Hotstar"},
            "hotstar": {"id": 3, "name": "Disney+ Hotstar"},
            "zee5": {"id": 4, "name": "ZEE5"},
            "sun nxt": {"id": 5, "name": "Sun NXT"},
            "aha": {"id": 6, "name": "Aha"},
            "jio cinema": {"id": 7, "name": "JioCinema"},
            "sony liv": {"id": 8, "name": "SonyLIV"},
        }
        seen = set()
        for keyword, info in ott_map.items():
            if keyword in text and info["id"] not in seen:
                seen.add(info["id"])
                providers.append(info)

        return providers

    async def get_movie_details(self, source_id: str) -> Optional[Movie]:
        """Fetch detailed movie info from Wikipedia page."""
        cache_key = f"wiki_movie_details_scrapling_{source_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return Movie(
                source="wikipedia",
                source_id=cached.get("source_id", source_id),
                title=cached["title"],
                year=cached["year"],
                poster_url=cached["poster_url"],
                overview=cached["overview"],
            )

        html = await self._get_page_html_by_id(source_id)
        if not html:
            return None

        response = Selector(html, url=f"https://en.wikipedia.org/?curid={source_id}" if source_id.isdigit() else f"https://en.wikipedia.org/wiki/{source_id.replace(' ', '_')}")
        
        # Extract title from #firstHeading
        title_element = response.css("#firstHeading::text").get()
        if not title_element:
            title_element = response.css("h1::text").get()
        
        title_text = str(title_element) if title_element else ""
        clean_title, year = self._parse_film_title(title_text)

        # Resolve numeric page ID
        resolved_source_id = source_id
        shortlink = response.css('link[rel="shortlink"]::attr(href)').get()
        if shortlink:
            match = re.search(r'curid=(\d+)', str(shortlink))
            if match:
                resolved_source_id = match.group(1)

        # Extract poster
        poster_url = None
        img_src = response.css(".infobox-image img::attr(src)").get() or response.css(".infobox img::attr(src)").get()
        if img_src:
            poster_url = response.urljoin(str(img_src))

        # Extract overview (first few paragraphs of lead section)
        overview_parts = []
        for p in response.css(".mw-parser-output > p"):
            p_text = p.get_all_text(separator="", strip=True)
            # Remove citation brackets like [1], [2], etc.
            p_text = re.sub(r"\[\d+\]", "", p_text)
            if p_text:
                overview_parts.append(p_text)
                if len(" ".join(overview_parts)) >= 500:
                    break
        overview = " ".join(overview_parts)[:500] if overview_parts else None

        movie_dict = {
            "source_id": resolved_source_id,
            "title": clean_title,
            "year": year,
            "poster_url": poster_url,
            "overview": overview,
        }
        await api_cache.set(cache_key, "wikipedia_movie_details", movie_dict, 604800)

        return Movie(
            source="wikipedia",
            source_id=resolved_source_id,
            title=clean_title,
            year=year,
            poster_url=poster_url,
            overview=overview,
        )

    async def _get_page_html(self, title: str, lang: str = "en") -> Optional[str]:
        """Fetch rendered HTML of a Wikipedia page."""
        return await self._get_page_html_by_id(title, lang=lang)

    async def _get_page_html_by_id(self, page_id: str, lang: str = "en") -> Optional[str]:
        """Fetch rendered HTML of a Wikipedia page by page ID or title."""
        if page_id.isdigit():
            url = f"https://{lang}.wikipedia.org/?curid={page_id}"
        else:
            url = f"https://{lang}.wikipedia.org/wiki/{page_id.replace(' ', '_')}"
            
        cache_key = f"wiki_html_id_{lang}_{page_id}"
        cached = await api_cache.get(cache_key)
        if cached is not None:
            return cached

        await rate_limiter.acquire("wikipedia")
        t0 = time.time()
        try:
            resp = await AsyncFetcher.get(url, headers={"User-Agent": USER_AGENT})
            ms = int((time.time() - t0) * 1000)
            if resp.status == 200:
                html = resp.get()
                providers_logger.info(
                    f"provider=wikipedia_id_direct latency={ms}ms success=True"
                )
                await api_cache.set(cache_key, "wikipedia_id_direct", html, 604800)
                return html
            providers_logger.error(
                f"provider=wikipedia_id_direct latency={ms}ms success=False status={resp.status}"
            )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            providers_logger.error(
                f'provider=wikipedia_id_direct latency={ms}ms success=False error="{e}"'
            )
            logger.error(f"Wikipedia ID page fetch failed: {e}")
        return None

    def _parse_film_list_page(self, html: str) -> List[tuple]:
        """Parse a 'List of Tamil films of YYYY' Wikipedia page.
        Returns a list of (Movie, Optional[datetime.date]) tuples."""
        soup = Selector(html)
        movies = []
        import datetime

        current_year = datetime.datetime.now().year

        for table in soup.find_all("table", class_="wikitable"):
            rows = table.find_all("tr")
            if not rows:
                continue

            # Get headers with colspan expansion
            header_row = rows[0]
            headers_text = []
            for th in header_row.find_all("th"):
                colspan = int(th.attrib.get("colspan", 1))
                text = th.get_all_text(separator="", strip=True).lower()
                headers_text.extend([text] * colspan)

            if "title" not in headers_text:
                continue

            title_idx = headers_text.index("title")
            rowspans = [0] * len(headers_text)

            current_month = ""
            current_date_num = ""

            for row in rows[1:]:
                if row.find("th") and not row.find("td"):
                    continue

                raw_cells = row.find_all(["td", "th"])
                if not raw_cells:
                    continue

                row_cells = [None] * len(headers_text)
                raw_idx = 0
                for col_idx in range(len(headers_text)):
                    if rowspans[col_idx] > 0:
                        rowspans[col_idx] -= 1
                        row_cells[col_idx] = "SPANNED"
                    else:
                        if raw_idx < len(raw_cells):
                            cell = raw_cells[raw_idx]
                            raw_idx += 1
                            row_cells[col_idx] = cell

                            # Check for rowspan
                            rowspan_val = cell.attrib.get("rowspan")
                            if rowspan_val:
                                try:
                                    rowspans[col_idx] = int(rowspan_val) - 1
                                except ValueError:
                                    rowspans[col_idx] = 0

                # Update date tracking (Column 0 is month if present, Column 1 is date if present)
                if row_cells[0] and row_cells[0] != "SPANNED":
                    current_month = row_cells[0].get_all_text(separator="", strip=True)
                if row_cells[1] and row_cells[1] != "SPANNED":
                    current_date_num = row_cells[1].get_all_text(separator="", strip=True)

                title_cell = row_cells[title_idx]
                if title_cell and title_cell != "SPANNED":
                    link = title_cell.find("a")
                    title = (
                        link.get_all_text(separator="", strip=True)
                        if link
                        else title_cell.get_all_text(separator="", strip=True)
                    )
                    title = title.strip()
                    if title and title != "-" and len(title) > 1:
                        # Store page title in source_id temporarily for batch resolution
                        page_title = (
                            link.attrib.get("title") if (link and "title" in link.attrib) else title
                        )

                        rel_date = self._parse_wikipedia_date(
                            current_month, current_date_num, current_year
                        )
                        movies.append(
                            (
                                Movie(
                                    source="wikipedia",
                                    source_id=page_title,
                                    title=title,
                                    year=current_year,
                                    language="ta",
                                ),
                                rel_date,
                            )
                        )

        return movies

    @staticmethod
    def _parse_wikipedia_date(
        month_str: str, date_str: str, year: int
    ) -> Optional[datetime.date]:
        """Convert Wikipedia month and day columns into a datetime.date object."""
        import datetime

        try:
            months_map = {
                "january": 1,
                "february": 2,
                "march": 3,
                "april": 4,
                "may": 5,
                "june": 6,
                "july": 7,
                "august": 8,
                "september": 9,
                "october": 10,
                "november": 11,
                "december": 12,
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12,
            }
            month_clean = re.sub(r"[^a-zA-Z]", "", month_str).lower()
            month_num = months_map.get(month_clean)
            if not month_num:
                return None

            date_clean = re.search(r"\d+", date_str)
            if not date_clean:
                return None
            day_num = int(date_clean.group(0))

            return datetime.date(year, month_num, day_num)
        except Exception:
            return None

    @staticmethod
    def _is_film_page(title: str, snippet: str) -> bool:
        """Check if a Wikipedia page is about a film."""
        combined = f"{title} {snippet}".lower()
        film_indicators = [
            "film",
            "movie",
            "cinema",
            "திரைப்படம்",
            "directed by",
            "starring",
        ]
        return any(ind in combined for ind in film_indicators)

    @staticmethod
    def _parse_film_title(title: str) -> tuple:
        """Extract clean title and year from 'Movie (2024 film)' format."""
        match = re.match(r"^(.+?)\s*\((\d{4})\s*(?:film|movie|திரைப்படம்)?\)", title)
        if match:
            return match.group(1).strip(), int(match.group(2))
        # Try just year in parentheses
        match = re.match(r"^(.+?)\s*\((\d{4})\)", title)
        if match:
            return match.group(1).strip(), int(match.group(2))
        return title.strip(), None
