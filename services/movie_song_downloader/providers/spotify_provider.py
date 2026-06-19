import httpx
import re
import json
import logging
from typing import Tuple, List, Optional
from movie_song_downloader.core.models import Movie, Album, Track

logger = logging.getLogger("movie_song_downloader.SpotifyProvider")


class SpotifyProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

    def _get_cover_url(self, vi: dict) -> Optional[str]:
        if not vi or "image" not in vi:
            return None
        images = vi["image"]
        if not images:
            return None
        # Sort images by maxWidth/maxHeight descending to get the best quality
        sorted_imgs = sorted(
            images,
            key=lambda x: (x.get("maxWidth", 0) or 0) * (x.get("maxHeight", 0) or 0),
            reverse=True,
        )
        return sorted_imgs[0].get("url")

    async def get_spotify_album_or_track(
        self, spotify_url_or_id: str
    ) -> Tuple[Movie, Album, List[Track]]:
        """
        Parses the Spotify URL or ID to scrape the public embed metadata.
        Returns:
            Tuple[Movie, Album, List[Track]]
        """
        # Detect ID and Type
        match = re.search(r"(album|track)/([a-zA-Z0-9]+)", spotify_url_or_id)
        if match:
            item_type = match.group(1)
            item_id = match.group(2)
        else:
            # Assume it's a raw ID, default to album
            item_type = "album"
            item_id = spotify_url_or_id

        embed_url = f"https://open.spotify.com/embed/{item_type}/{item_id}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(embed_url, headers=self.headers)
            if resp.status_code != 200:
                raise Exception(
                    f"Failed to fetch Spotify embed page: status {resp.status_code}"
                )

        html = resp.text
        json_match = re.search(
            r'<script id="__NEXT_DATA__"[^>]* type="application/json">(.*?)</script>',
            html,
            re.DOTALL,
        )
        if not json_match:
            raise Exception(
                "Failed to extract metadata from Spotify embed page: __NEXT_DATA__ not found."
            )

        try:
            data = json.loads(json_match.group(1))
        except Exception as e:
            raise Exception(f"Failed to parse Spotify embed JSON metadata: {e}")

        state_data = (
            data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {})
        )
        entity = state_data.get("entity", {})
        if not entity:
            raise Exception("Invalid Spotify embed JSON structure: 'entity' not found.")

        # Check for error status
        if data.get("props", {}).get("pageProps", {}).get("status") == 404:
            raise Exception("Spotify item not found (404). Check the URL/ID.")

        title = entity.get("title") or entity.get("name") or "Unknown"
        cover_url = self._get_cover_url(entity.get("visualIdentity", {}))

        if item_type == "album":
            artist_name = entity.get("subtitle") or "Unknown Artist"
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Album: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=len(entity.get("trackList", [])),
            )

            tracks = []
            for idx, t in enumerate(entity.get("trackList", []), start=1):
                t_uri = t.get("uri", "")
                t_id = t_uri.split(":")[-1] if ":" in t_uri else t.get("uid", "")

                # Extract preview URL if available
                preview_url = (
                    t.get("audioPreview", {}).get("url")
                    if t.get("audioPreview")
                    else None
                )

                tracks.append(
                    Track(
                        source="spotify",
                        source_id=t_id,
                        spotify_id=t_id,
                        title=t.get("title", "Unknown Track"),
                        artist=t.get("subtitle") or artist_name,
                        duration_ms=t.get("duration", 0),
                        track_number=idx,
                        preview_url=preview_url,
                    )
                )
            return movie, album, tracks

        else:  # track
            artists_list = entity.get("artists", [])
            artist_name = (
                ", ".join([a.get("name", "") for a in artists_list])
                if artists_list
                else "Unknown Artist"
            )

            # For a single track, wrap it in a dummy album of size 1
            movie = Movie(
                source="spotify",
                source_id=item_id,
                title=title,
                poster_url=cover_url,
                overview=f"Spotify Track: {title} by {artist_name}",
            )
            album = Album(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                cover_url=cover_url,
                total_tracks=1,
            )

            preview_url = (
                entity.get("audioPreview", {}).get("url")
                if entity.get("audioPreview")
                else None
            )

            track = Track(
                source="spotify",
                source_id=item_id,
                spotify_id=item_id,
                title=title,
                artist=artist_name,
                duration_ms=entity.get("duration", 0),
                track_number=1,
                preview_url=preview_url,
            )
            return movie, album, [track]
