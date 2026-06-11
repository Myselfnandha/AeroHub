-- Migration: 002_provider_health
-- Date: 2026-06-02

CREATE TABLE IF NOT EXISTS provider_health (
    provider TEXT NOT NULL,
    category TEXT NOT NULL,      -- movie | soundtrack | lyrics | download
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    total_latency_ms INTEGER DEFAULT 0,
    last_checked TEXT,
    PRIMARY KEY (provider, category)
);
