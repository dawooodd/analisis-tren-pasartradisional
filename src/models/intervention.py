"""Interrupted Time Series (ITS) panel untuk mengukur guncangan COVID-19.

Y_it = b0 + b1*t + b2*COVID_t + b3*(t-2020)*POST_t + a_i + e_it
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ITSResult:
    level_shift: float          # b2
    slope_change: float         # b3
    ci95: dict[str, tuple[float, float]]
    per_wilayah: pd.DataFrame   # shock_magnitude, recovery_rate per kab/kota


def fit_its_panel(panel: pd.DataFrame, target: str) -> ITSResult:
    """Fixed-effects ITS dengan clustered SE per kab/kota."""
    raise NotImplementedError("Dijadwalkan pada fase pemodelan")


def recovery_rate(actual_2024: float, trough: float, counterfactual_2024: float) -> float:
    """RR = (Y_2024 - Y_trough) / (Ŷ_2024|tren pra-COVID - Y_trough). RR>=1 → pulih penuh."""
    denom = counterfactual_2024 - trough
    if denom == 0:
        return float("nan")
    return (actual_2024 - trough) / denom
