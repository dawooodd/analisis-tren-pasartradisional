"""Survival analysis penutupan pasar (aktif bila tersedia data tingkat pasar)."""

from __future__ import annotations

import pandas as pd


def fit_cox(df: pd.DataFrame, duration_col: str, event_col: str, covariates: list[str]):
    """Cox Proportional Hazards (lifelines); evaluasi C-index."""
    raise NotImplementedError("Dijadwalkan pada fase pemodelan")
