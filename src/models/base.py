"""Antarmuka bersama seluruh model agar dapat dibandingkan & di-ensemble secara seragam."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class ForecastResult:
    """Output standar forecast (long-format)."""

    #: kolom: kode_wilayah, tahun, indikator, yhat, yhat_lower_80, yhat_upper_80,
    #:        yhat_lower_95, yhat_upper_95, model, skenario
    frame: pd.DataFrame
    meta: dict[str, Any] = field(default_factory=dict)


class BaseForecaster(ABC):
    """Kontrak model time-series/panel."""

    name: str = "base"

    @abstractmethod
    def fit(self, panel: pd.DataFrame, target: str, exog: list[str] | None = None) -> BaseForecaster:
        ...

    @abstractmethod
    def predict(self, horizon: int, skenario: str = "baseline") -> ForecastResult:
        ...
