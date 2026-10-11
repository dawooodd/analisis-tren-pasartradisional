"""Kontrak komponen visual. Implementasi dijadwalkan pada fase visualisasi."""

from __future__ import annotations

import pandas as pd

from components.sidebar import FilterState


def kpi_row(panel: pd.DataFrame | None, f: FilterState) -> None:
    """4 kartu: total pasar aktif, total pedagang, rata-rata MDI, jumlah kab/kota zona merah."""
    raise NotImplementedError


def choropleth(panel: pd.DataFrame, gdf, f: FilterState, animate: bool = True):
    """Peta 38 kab/kota (plotly choropleth_mapbox) + overlay klaster LISA."""
    raise NotImplementedError


def ecommerce_vs_lapak(panel: pd.DataFrame, f: FilterState):
    """Dual-axis: lapak/pedagang aktif vs. indeks e-commerce, shading PSBB/PPKM, garis kontrafaktual."""
    raise NotImplementedError


def shock_recovery_quadrant(its_per_wilayah: pd.DataFrame):
    """Scatter shock magnitude vs. recovery rate (Resilient/Recovered/Fragile/Scarred)."""
    raise NotImplementedError


def forecast_fan(forecast: pd.DataFrame, f: FilterState):
    """Fan chart proyeksi 2025-2029 dengan PI 80% & 95%."""
    raise NotImplementedError
