-- Migration: 005_release_date_enrichment
-- Date: 2026-06-04
-- Adds release_date to movies, composer to albums, and isrc to tracks

ALTER TABLE movies ADD COLUMN release_date TEXT;
ALTER TABLE albums ADD COLUMN composer TEXT;
ALTER TABLE tracks ADD COLUMN isrc TEXT;
