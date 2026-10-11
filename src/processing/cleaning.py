"""Pembersihan data mentah: tipe data, duplikasi, outlier administratif."""

from __future__ import annotations

import pandas as pd


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Satu nilai per (kode_wilayah, tahun, indikator); prioritas sumber mengikuti fallback chain."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")


def flag_outliers(df: pd.DataFrame, z: float = 3.5) -> pd.DataFrame:
    """Tandai lonjakan tidak wajar (robust z-score per wilayah-indikator) → kolom `is_outlier`."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")
