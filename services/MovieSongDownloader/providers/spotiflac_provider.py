import os
import httpx
import re
import logging
import asyncio
import shutil
from typing import Optional, Callable
from urllib.parse import quote_plus

from MovieSongDownloader.providers.base import BaseDownloadProvider
from MovieSongDownloader.core.models import Track
from MovieSongDownloader.core.settings_manager import settings_manager

logger = logging.getLogger("MovieSongDownloader.SpotiFLACProvider")


class SpotiFLACProvider(BaseDownloadProvider):
    def _get_subprocess_env(self) -> dict:
        """
        Prepares environment variables for subprocesses, ensuring ffmpeg is in PATH
        and preventing UnicodeEncodeError in python CLI tools.
        """
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        
        # Add local bin directory to PATH
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bin_dir = os.path.join(base_dir, "bin")
        if os.path.exists(bin_dir):
            env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
            
        return env

    async def _resolve_spotify_url(self, title: str, artist: str) -> str:
        """
        Queries DuckDuckGo HTML search to resolve a song's title & artist to a Spotify track URL.
        """
        clean_title = title.replace('"', "").replace("'", "")
        clean_artist = artist.split(",")[0].strip()
        query = f'site:open.spotify.com/track "{clean_artist}" "{clean_title}"'
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        logger.info(
            f"Resolving Spotify track URL for '{title}' by '{artist}' via DDG..."
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(f"Resolved track successfully to: {resolved_url}")
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify resolution request failed: {e}")

        # Fallback to a broader search query if exact match failed
        query_broad = f"site:open.spotify.com/track {clean_artist} {clean_title}"
        url_broad = f"https://html.duckduckgo.com/html/?q={quote_plus(query_broad)}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url_broad, headers=headers)
                if resp.status_code == 200:
                    matches = re.findall(
                        r"open\.spotify\.com/track/([a-zA-Z0-9]+)", resp.text
                    )
                    if matches:
                        spotify_id = matches[0]
                        resolved_url = f"https://open.spotify.com/track/{spotify_id}"
                        logger.info(
                            f"Resolved track via broad query to: {resolved_url}"
                        )
                        return resolved_url
        except Exception as e:
            logger.error(f"DDG Spotify broad resolution request failed: {e}")

        raise Exception(
            f"Could not resolve a Spotify track URL for '{title}' by '{artist}'."
        )

    async def _transcode_audio(
        self, input_path: str, output_path: str, format_str: str, bitrate: str = "320"
    ) -> None:
        """
        Transcodes the input audio file to the target format using ffmpeg.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ffmpeg_path = os.path.join(base_dir, "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = "ffmpeg"  # fallback to path

        format_str = format_str.lower()
        cmd = [ffmpeg_path, "-y", "-i", input_path, "-vn"]

        if format_str == "mp3":
            cmd.extend(["-ar", "44100", "-ac", "2", "-b:a", f"{bitrate}k", output_path])
        elif format_str == "flac":
            cmd.extend([output_path])
        elif format_str in ("m4a", "aac"):
            cmd.extend(["-c:a", "copy", output_path])
        else:
            cmd.extend([output_path])

        logger.info(f"SpotiFLAC Transcode: {' '.join(cmd)}")
        env = self._get_subprocess_env()
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"ffmpeg transcoding failed: {err_msg}")
            raise Exception(f"Transcoding failed: {err_msg}")

    async def download(
        self,
        track: Track,
        format: str,
        output_dir: str,
        filename_template: str,
        on_progress: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        """
        Downloads a track using spotiflac globally installed CLI command.
        """
        # Resolve Spotify track URL
        if track.source == "spotify" and track.source_id:
            spotify_url = f"https://open.spotify.com/track/{track.source_id}"
        else:
            spotify_url = await self._resolve_spotify_url(track.title, track.artist)

        # We will download the track into a temporary subfolder to identify the generated file
        temp_subfolder = os.path.join(
            output_dir, f"spotiflac_temp_{track.source_id or 'unknown'}"
        )
        if os.path.exists(temp_subfolder):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
        os.makedirs(temp_subfolder, exist_ok=True)

        if on_progress:
            on_progress(20.0, "spotiflac_starting")

        cmd = ["spotiflac", spotify_url, temp_subfolder]

        # Check settings for Deezer ARL or other service prioritization (optional parameter)
        deezer_arl = await settings_manager.get("deezer_arl")
        # We can specify service priority or other custom flags if desired
        # e.g., --service deezer
        services = []
        if deezer_arl:
            # If Deezer ARL is configured, we prioritize deezer download
            services.append("deezer")

        # Default priority: tidal, qobuz, deezer, amazon
        # We can pass them as args if spotiflac CLI supports --service flag
        if services:
            cmd.extend(["--service"] + services)

        logger.info(f"Executing SpotiFLAC Command: {' '.join(cmd)}")

        if on_progress:
            on_progress(40.0, "spotiflac_downloading")

        try:
            env = self._get_subprocess_env()
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
            )
            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode(errors="ignore")
            stderr_str = stderr.decode(errors="ignore")

            logger.info(f"spotiflac stdout: {stdout_str}")
            if process.returncode != 0:
                logger.error(f"spotiflac stderr: {stderr_str}")
                raise Exception(
                    f"SpotiFLAC download failed with exit code {process.returncode}: {stderr_str}"
                )

        except Exception as e:
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise e

        if on_progress:
            on_progress(80.0, "spotiflac_postprocessing")

        # Scan for the downloaded audio file
        audio_extensions = (".flac", ".mp3", ".m4a", ".aac", ".ogg", ".wav")
        downloaded_file = None
        for root, _, files in os.walk(temp_subfolder):
            for file in files:
                if file.lower().endswith(audio_extensions):
                    downloaded_file = os.path.join(root, file)
                    break
            if downloaded_file:
                break

        if not downloaded_file or not os.path.exists(downloaded_file):
            shutil.rmtree(temp_subfolder, ignore_errors=True)
            raise Exception(
                "SpotiFLAC executed successfully, but no audio file was generated in the output directory."
            )

        # Resolve target path in output_dir
        file_ext = os.path.splitext(downloaded_file)[1].lower()
        target_ext = f".{format.lower()}"

        # Check if we need transcoding (e.g. SpotiFLAC downloaded FLAC but format is MP3)
        if file_ext != target_ext:
            logger.info(
                f"Transcoding SpotiFLAC output {file_ext} to target {target_ext}..."
            )
            bitrate = await settings_manager.get("bitrate") or "320"
            temp_transcoded = os.path.join(temp_subfolder, f"transcoded{target_ext}")
            await self._transcode_audio(
                downloaded_file, temp_transcoded, format, bitrate
            )
            downloaded_file = temp_transcoded

        # Copy the file to the parent output_dir (or return its path so download_service moves it)
        final_temp_path = os.path.join(
            output_dir, f"spotiflac_result_{track.source_id}{target_ext}"
        )
        if os.path.exists(final_temp_path):
            os.remove(final_temp_path)

        shutil.move(downloaded_file, final_temp_path)
        shutil.rmtree(temp_subfolder, ignore_errors=True)

        return final_temp_path
