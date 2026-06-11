-- Migration: 001_initial
-- Date: 2026-06-02

-- Create schema_migrations tracker
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now'))
);

-- Movies Business Data
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    year INTEGER,
    poster_url TEXT,
    poster_cached_path TEXT,
    overview TEXT,
    language TEXT,
    genres TEXT,          -- JSON Array of string
    ott_providers TEXT,   -- JSON Array of dicts
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_movies_tmdb ON movies(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(year);

-- Albums Business Data
CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    cover_url TEXT,
    cover_cached_path TEXT,
    total_tracks INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_albums_spotify ON albums(spotify_id);
CREATE INDEX IF NOT EXISTS idx_albums_movie ON albums(movie_id);

-- Tracks Business Data
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
    spotify_id TEXT UNIQUE,
    title TEXT NOT NULL,
    artist TEXT,
    duration_ms INTEGER,
    track_number INTEGER,
    preview_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tracks_spotify ON tracks(spotify_id);
CREATE INDEX IF NOT EXISTS idx_tracks_album ON tracks(album_id);

-- Download Job Queue
CREATE TABLE IF NOT EXISTS download_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'queued', -- queued, downloading, fetching_lyrics, embedding_cover, embedding_metadata, saving_lrc, generating_playlist, completed, failed, paused, cancelled
    progress REAL DEFAULT 0.0,
    output_path TEXT,
    format TEXT DEFAULT 'mp3',
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON download_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_track ON download_jobs(track_id);

-- Lyrics Fallback Output Results
CREATE TABLE IF NOT EXISTS lyrics_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER REFERENCES tracks(id) ON DELETE CASCADE,
    provider TEXT,        -- lrclib | syncedlyrics | musixmatch | genius
    lyrics_type TEXT,     -- synced | plain | none
    content TEXT,
    confidence REAL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_lyrics_track ON lyrics_results(track_id);

-- Watchlist tracker
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    expected_release TEXT,
    last_checked TEXT,
    auto_download INTEGER DEFAULT 1,
    status TEXT DEFAULT 'watching', -- watching | found | downloaded | expired
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_watchlist_tmdb ON watchlist(tmdb_id);

-- Settings Key-Value Configuration Store
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_settings_category ON settings(category);

-- Download Deduplication Cache
CREATE TABLE IF NOT EXISTS download_cache (
    track_hash TEXT PRIMARY KEY, -- SHA256(artist + title + album + duration)
    file_path TEXT NOT NULL,
    format TEXT NOT NULL,
    downloaded_at TEXT DEFAULT (datetime('now'))
);

-- Raw API Response Cache (Metadata cache decoupling)
CREATE TABLE IF NOT EXISTS api_cache (
    cache_key TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    json_payload TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_api_cache_expires ON api_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_api_cache_provider ON api_cache(provider);
