"""Imputasi data hilang pada panel. Setiap nilai imputasi WAJIB ditandai `is_imputed=True`."""

from __future__ import annotations

from typing import Literal

import pandas as pd

Method = Literal["linear", "panel_mean_growth", "none"]


def impute(df: pd.DataFrame, method: Method = "linear", max_gap: int = 2) -> pd.DataFrame:
    """Isi celah ≤ `max_gap` tahun per wilayah-indikator; celah lebih panjang dibiarkan NaN."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")
