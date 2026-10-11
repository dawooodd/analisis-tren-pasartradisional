"""Harmonisasi lintas tahun & sumber: satuan, definisi, perubahan tahun dasar."""

from __future__ import annotations

import pandas as pd


def harmonize_units(df: pd.DataFrame) -> pd.DataFrame:
    """Konversi ke satuan kanonik di `config/indicators.yaml`."""
    raise NotImplementedError("Dijadwalkan pada fase ETL")


def to_wide_panel(df: pd.DataFrame) -> pd.DataFrame:
    """Long → wide: index (kode_wilayah, tahun), kolom = indikator."""
    return df.pivot_table(index=["kode_wilayah", "tahun"], columns="indikator",
                          values="nilai", aggfunc="first").reset_index()
