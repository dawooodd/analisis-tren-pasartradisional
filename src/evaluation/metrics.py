"""Metrik evaluasi forecast."""

from __future__ import annotations

import numpy as np


def smape(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    mask = denom != 0
    return float(np.mean(np.abs(y_true - y_pred)[mask] / denom[mask]) * 100)


def mase(y_true, y_pred, y_train, m: int = 1) -> float:
    """MASE terhadap naive forecast lag-m (metrik utama: skala-bebas antarwilayah)."""
    y_true, y_pred, y_train = (np.asarray(a, float) for a in (y_true, y_pred, y_train))
    scale = np.mean(np.abs(y_train[m:] - y_train[:-m]))
    return float(np.mean(np.abs(y_true - y_pred)) / scale) if scale else float("nan")


def interval_coverage(y_true, lower, upper) -> float:
    y_true, lower, upper = (np.asarray(a, float) for a in (y_true, lower, upper))
    return float(np.mean((y_true >= lower) & (y_true <= upper)))
