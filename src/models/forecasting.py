"""Implementasi forecaster: SARIMAX, Prophet, model global (pooled), dan ensemble."""

from __future__ import annotations

import pandas as pd

from src.models.base import BaseForecaster, ForecastResult


class SarimaxForecaster(BaseForecaster):
    name = "sarimax"

    def fit(self, panel: pd.DataFrame, target: str, exog: list[str] | None = None):
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")

    def predict(self, horizon: int, skenario: str = "baseline") -> ForecastResult:
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")


class ProphetForecaster(BaseForecaster):
    """Untuk seri bulanan; changepoint manual 2020-03 & 2022-01."""

    name = "prophet"

    def fit(self, panel: pd.DataFrame, target: str, exog: list[str] | None = None):
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")

    def predict(self, horizon: int, skenario: str = "baseline") -> ForecastResult:
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")


class GlobalPooledForecaster(BaseForecaster):
    """Satu model untuk 38 wilayah (mengatasi seri tahunan pendek, n=11)."""

    name = "global_pooled"

    def fit(self, panel: pd.DataFrame, target: str, exog: list[str] | None = None):
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")

    def predict(self, horizon: int, skenario: str = "baseline") -> ForecastResult:
        raise NotImplementedError("Dijadwalkan pada fase pemodelan")


def ensemble(results: list[ForecastResult], weights: dict[str, float]) -> ForecastResult:
    """Rata-rata tertimbang (bobot = inverse-MASE dari backtesting)."""
    raise NotImplementedError("Dijadwalkan pada fase pemodelan")
