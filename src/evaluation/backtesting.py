"""Rolling-origin backtesting.

Skema default:
- Origin 2019 → uji 2020-2021 (ketahanan terhadap guncangan)
- Origin 2021 → uji 2022-2024 (kemampuan menangkap pemulihan)
"""

from __future__ import annotations

import pandas as pd

from src.models.base import BaseForecaster

DEFAULT_ORIGINS: list[tuple[int, int]] = [(2019, 2), (2021, 3)]  # (tahun_akhir_train, horizon)


def backtest(model: BaseForecaster, panel: pd.DataFrame, target: str,
             origins: list[tuple[int, int]] = DEFAULT_ORIGINS) -> pd.DataFrame:
    """Return metrik per origin & per wilayah (MASE, sMAPE, coverage)."""
    raise NotImplementedError("Dijadwalkan pada fase pemodelan")
