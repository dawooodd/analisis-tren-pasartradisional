"""Loader: data/raw/**/*.records.jsonl → DataFrame long-format terstandar."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.io import resolve_path


def iter_record_files(raw_dir: Path | None = None) -> list[Path]:
    """Seluruh file `*.records.jsonl` hasil emit agen."""
    return sorted((raw_dir or resolve_path("raw")).rglob("*.records.jsonl"))


def load_raw_records(raw_dir: Path | None = None) -> pd.DataFrame:
    """Gabungkan seluruh record mentah menjadi satu DataFrame long-format."""
    files = iter_record_files(raw_dir)
    if not files:
        return pd.DataFrame(
            columns=["kode_wilayah", "tahun", "indikator", "nilai", "satuan",
                     "sumber", "url_sumber", "diambil_pada", "is_imputed"]
        )
    return pd.concat((pd.read_json(f, lines=True, dtype={"kode_wilayah": str})
                      for f in files), ignore_index=True)
