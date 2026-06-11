-- Migration: 003_cache
-- Date: 2026-06-02

-- Unified search index virtual table (FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
    source,        -- tmdb | spotify
    source_id,     -- external ID
    title,
    artist,
    year,
    type           -- movie | album | track
);
