from MovieSongDownloader.providers.metadata_normalizer import (
    normalize_title,
    confidence_score,
)


def test_normalize_title():
    # Suffixes should be stripped
    assert normalize_title("Naan Ready (From Leo)") == "Naan Ready"
    assert (
        normalize_title("Inception (Original Motion Picture Soundtrack)") == "Inception"
    )
    assert normalize_title("Song Title (Official Audio)") == "Song Title"
    assert normalize_title("Remastered Track (Remastered 2020)") == "Remastered Track"
    assert normalize_title("Featured Track (feat. Artist Name)") == "Featured Track"

    # Normal title should remain untouched
    assert normalize_title("Stay") == "Stay"


def test_confidence_score_exact():
    source = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    target = {
        "title": "Leo Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Exact match should score high
    score = confidence_score(source, target)
    assert score == 100


def test_confidence_score_close():
    source = {
        "title": "Naan Ready (From Leo)",
        "artist": "Anirudh Ravichander",
        "album": "Leo",
        "duration_ms": 241000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Close match with cleanable suffix, close artist string, and minor duration delta (1s) should score >= 80
    score = confidence_score(source, target)
    assert score >= 80


def test_confidence_score_different():
    source = {
        "title": "Different Song",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 180000,
    }
    target = {
        "title": "Naan Ready",
        "artist": "Anirudh",
        "album": "Leo",
        "duration_ms": 240000,
    }
    # Completely different tracks should score low
    score = confidence_score(source, target)
    assert score < 60
