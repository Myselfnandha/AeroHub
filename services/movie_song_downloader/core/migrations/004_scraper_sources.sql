-- Migration: 004_scraper_sources
-- Date: 2026-06-03
-- Adds source tracking columns for Wikipedia/JioSaavn/OMDb migration

-- Movies: add source tracking + enrichment fields
ALTER TABLE movies ADD COLUMN source TEXT DEFAULT 'wikipedia';
ALTER TABLE movies ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE movies ADD COLUMN rating TEXT;
ALTER TABLE movies ADD COLUMN cast_info TEXT;

-- Albums: add source tracking
ALTER TABLE albums ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE albums ADD COLUMN source_id TEXT DEFAULT '';

-- Tracks: add source tracking + direct download URL
ALTER TABLE tracks ADD COLUMN source TEXT DEFAULT 'jiosaavn';
ALTER TABLE tracks ADD COLUMN source_id TEXT DEFAULT '';
ALTER TABLE tracks ADD COLUMN download_url TEXT;

-- Watchlist: add generic source_id
ALTER TABLE watchlist ADD COLUMN source_id TEXT DEFAULT '';
