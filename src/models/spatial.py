"""Analisis spasial: Moran's I global, LISA, dan (M)GWR."""

from __future__ import annotations

import pandas as pd


def build_weights(gdf, method: str = "queen"):
    """Matriks bobot spasial dari GeoDataFrame 38 kab/kota."""
    raise NotImplementedError("Dijadwalkan pada fase analisis")


def global_moran(gdf, col: str, w=None) -> dict[str, float]:
    """Return: I, expected_I, p_sim."""
    raise NotImplementedError("Dijadwalkan pada fase analisis")


def local_moran(gdf, col: str, w=None) -> pd.DataFrame:
    """Klaster LISA per wilayah: HH / LL / HL / LH / NS."""
    raise NotImplementedError("Dijadwalkan pada fase analisis")


def fit_gwr(gdf, target: str, features: list[str]):
    """Koefisien lokal: apakah pengaruh e-commerce/ritel modern berbeda antarkawasan."""
    raise NotImplementedError("Dijadwalkan pada fase analisis")
