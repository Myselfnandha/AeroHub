from pathlib import Path

APP_NAME = "MovieSongDownloader"
APP_VERSION = "2.0.0"

APP_DIR = Path(__file__).resolve().parent
DATABASE_DIR = APP_DIR / ".db"
DATABASE_PATH = DATABASE_DIR / "db.sqlite3"
SETTINGS_BACKUP_PATH = DATABASE_DIR / "settings_backup.json"

LOGS_DIR = APP_DIR / ".logs"
CACHE_DIR = APP_DIR / ".cache"
POSTERS_CACHE_DIR = CACHE_DIR / "posters"
COVERS_CACHE_DIR = CACHE_DIR / "covers"

for directory in [
    DATABASE_DIR,
    LOGS_DIR,
    CACHE_DIR,
    POSTERS_CACHE_DIR,
    COVERS_CACHE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

APP_LOG_PATH = LOGS_DIR / "app.log"
DOWNLOADS_LOG_PATH = LOGS_DIR / "downloads.log"
PROVIDERS_LOG_PATH = LOGS_DIR / "providers.log"

DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Music" / "MovieSongDownloader")

# Data source URLs
WIKIPEDIA_EN_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_TA_API = "https://ta.wikipedia.org/w/api.php"
OMDB_BASE_URL = "https://www.omdbapi.com/"

DEFAULT_SETTINGS = {
    "omdb_api_key": "",
    "deezer_arl": "",
    "download_provider": "spotiflac",
    "scraping_limit": "5",
    "last_fetch_date": "",
    # Download
    "audio_format": "mp3",
    "bitrate": "320",
    "output_dir": DEFAULT_DOWNLOAD_DIR,
    "filename_format": "{TrackNum} - {Title}",
    "folder_format": "{Year}/{Movie}/Songs",
    "download_mode": "accurate",
    "max_concurrent": "2",
    # Lyrics
    "lyrics_priority": '["lrclib", "syncedlyrics", "musixmatch", "genius"]',
    "save_lrc_file": "true",
    "embed_lyrics": "true",
    # UI
    "theme": "dark",
    "default_tab": "home",
    "language_region": "en-US",
    # Watchlist
    "check_interval_hours": "24",
    "auto_download": "true",
    "notify_on_found": "true",
    # DNS (bypass ISP blocks)
    "doh_enabled": "true",
    "dns_provider": "cloudflare",
}

# Cyberpunk Cyan Design Tokens
COLOR_ACCENT = "#06B6D4"  # Cyan accent
COLOR_ACCENT_LIGHT = "#22D3EE"  # Light cyan for hover/focus
COLOR_TEXT_PRIMARY = "#FFFFFF"  # Crisp white
COLOR_TEXT_MUTED = "#94A3B8"  # Muted cool gray
COLOR_BG_PRIMARY = "#0B0F19"  # Deep dark blue/gray
COLOR_BG_SECONDARY = "#111827"  # Dark gray
COLOR_BORDER = "#1F2937"  # Dark gray border
