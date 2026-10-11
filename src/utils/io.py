"""Utilitas I/O terpusat: path proyek, pemuatan konfigurasi, dan setup logging.

Seluruh modul (agents, src, app) WAJIB mengambil path & parameter dari sini,
bukan meng-hardcode, agar pipeline konsisten di lokal, CI, dan deployment.
"""

from __future__ import annotations

import logging
import logging.config
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
CONFIG_DIR: Path = PROJECT_ROOT / "config"


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Muat file YAML; path relatif di-resolve terhadap root proyek."""
    p = Path(path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def load_settings() -> dict[str, Any]:
    return load_yaml(CONFIG_DIR / "settings.yaml")


def resolve_path(key: str) -> Path:
    """Ambil path absolut dari `settings.yaml > paths.<key>`."""
    return PROJECT_ROOT / load_settings()["paths"][key]


@lru_cache(maxsize=1)
def load_registry() -> list[dict[str, Any]]:
    """Daftar 38 kab/kota Jawa Timur dari registry agen."""
    return load_yaml(resolve_path("registry"))["wilayah"]


@lru_cache(maxsize=1)
def load_indicators() -> list[dict[str, Any]]:
    """Kamus indikator kanonik dari `config/indicators.yaml`."""
    return load_yaml(resolve_path("indicators"))["indikator"]


def load_env() -> None:
    """Muat variabel dari `.env` di root proyek (tanpa menimpa env yang sudah ada)."""
    try:
        from dotenv import load_dotenv
    except ImportError:  # pragma: no cover
        logging.getLogger(__name__).warning("python-dotenv tidak terpasang; .env diabaikan")
        return
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def setup_logging() -> None:
    """Muat `.env` lalu konfigurasi logging dari `config/logging.yaml` (idempoten)."""
    load_env()
    resolve_path("logs").mkdir(parents=True, exist_ok=True)
    cfg = load_yaml(CONFIG_DIR / "logging.yaml")
    for handler in cfg.get("handlers", {}).values():
        if "filename" in handler:
            handler["filename"] = str(PROJECT_ROOT / handler["filename"])
    logging.config.dictConfig(cfg)
