"""Utilitas geospasial: muat GeoJSON 38 kab/kota dan join ke panel via kode BPS."""

from __future__ import annotations

from src.utils.io import resolve_path


def load_geojson():
    """GeoDataFrame batas kab/kota Jatim; kolom kunci wajib `kode_wilayah` (4 digit BPS)."""
    import geopandas as gpd

    path = resolve_path("geojson")
    if not path.exists():
        raise FileNotFoundError(f"GeoJSON belum tersedia: {path}")
    return gpd.read_file(path)
