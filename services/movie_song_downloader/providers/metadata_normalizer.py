import re
from rapidfuzz import fuzz

NOISE_PATTERNS = [
    r"\(From\s+.*?\)",
    r"\(Remastered\s*\d*\)",
    r"\(Official\s+Audio\)",
    r"\[Extended\s+Version\]",
    r"\(Deluxe\s*Edition?\)",
    r"\(feat\.\s+.*?\)",
    r'\(From\s+"[^"]*"\)',
    r"\(Original\s+Motion\s+Picture\s+Soundtrack\)",
]


def normalize_title(title: str) -> str:
    # Strip Wikipedia parenthetical suffixes (e.g. "(film)", "(2026 film)", "(soundtrack)")
    title = re.sub(
        r"\s*\((?:film|\d{4}(?:\s+film)?|soundtrack|tamil\s+film|original\s+motion\s+picture\s+soundtrack|album)\)",
        "",
        title,
        flags=re.IGNORECASE,
    )

    for p in NOISE_PATTERNS:
        title = re.sub(p, "", title, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", title).strip()


def confidence_score(source: dict, target: dict) -> int:
    src_t = normalize_title(source.get("title", "")).lower()
    tgt_t = normalize_title(target.get("title", "")).lower()
    score = int(fuzz.ratio(src_t, tgt_t) * 0.50)
    score += int(
        fuzz.ratio(source.get("artist", "").lower(), target.get("artist", "").lower())
        * 0.30
    )
    sa, ta = source.get("album", "").lower(), target.get("album", "").lower()
    score += int(fuzz.ratio(sa, ta) * 0.10) if sa and ta else 10
    dur = abs(source.get("duration_ms", 0) - target.get("duration_ms", 0))
    score += 10 if dur <= 3000 else (5 if dur <= 5000 else (2 if dur <= 10000 else 0))
    return score
