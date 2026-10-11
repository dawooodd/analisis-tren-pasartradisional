"""Fitur turunan untuk pemodelan (input: wide panel)."""

from __future__ import annotations

import pandas as pd


def add_per_capita(df: pd.DataFrame, cols: list[str], per: int = 10_000) -> pd.DataFrame:
    """Normalisasi per `per` penduduk (mis. minimarket per 10.000 jiwa)."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")


def add_growth(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Pertumbuhan YoY (%) per wilayah."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")


def add_covid_dummies(df: pd.DataFrame, periode: tuple[int, int] = (2020, 2021)) -> pd.DataFrame:
    """Kolom `covid`, `post_covid`, `t_since_covid` untuk model ITS."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")
