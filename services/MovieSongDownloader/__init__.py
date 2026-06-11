# MovieSongDownloader Package Init

import os
import sys


# Synchronously bootstrap DoH DNS resolver to bypass ISP block.
# We do this at the very beginning of package import to override the socket resolution.
def _early_bootstrap_dns():
    import sqlite3
    from pathlib import Path

    app_dir = Path(__file__).resolve().parent
    db_path = app_dir / "db.sqlite3"
    doh_enabled = True
    dns_provider = "cloudflare"
    try:
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT key, value FROM settings WHERE key IN ('doh_enabled', 'dns_provider')"
            )
            rows = cursor.fetchall()
            for key, val in rows:
                if key == "doh_enabled":
                    doh_enabled = val == "true"
                elif key == "dns_provider":
                    dns_provider = val
            conn.close()
    except Exception:
        pass

    if doh_enabled:
        try:
            from MovieSongDownloader.core.dns_resolver import bootstrap_dns_sync

            bootstrap_dns_sync(dns_provider)
        except Exception as e:
            print(f"Error early-bootstrapping DoH DNS resolver: {e}", file=sys.stderr)


_early_bootstrap_dns()

# Apply runtime patches for Windows paths / ampersands inside yt-dlp & deezload
import yt_dlp  # noqa: E402

sys.modules["youtube_dl"] = yt_dlp

# Prepend local bin directory to system PATH for FFmpeg binaries
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

# Patch deezload query string parsing for Windows paths / ampersands
try:
    import deezload.base

    original_extract = deezload.base.extract_video_id

    def patched_extract_video_id(qs: str):
        try:
            qs_decoded = qs.encode("utf-8").decode("unicode-escape")
        except Exception:
            qs_decoded = qs
        qs_decoded = qs_decoded.replace(r"\u0026", "&").replace("\\u0026", "&")
        return original_extract(qs_decoded)

    deezload.base.extract_video_id = patched_extract_video_id
except Exception:
    pass
