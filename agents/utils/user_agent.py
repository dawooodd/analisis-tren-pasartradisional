"""Header HTTP standar untuk seluruh agen."""

from __future__ import annotations

from src.utils.io import load_settings


def default_headers() -> dict[str, str]:
    """User-Agent identifikatif (bukan menyamar sebagai browser) sesuai etika scraping."""
    return {
        "User-Agent": load_settings()["agents"]["user_agent"],
        "Accept": "application/json, text/html;q=0.9",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.5",
    }
