"""Lapisan akses data dashboard (cache Streamlit). Komponen visual TIDAK membaca file langsung."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.io import resolve_path


@st.cache_data(ttl=3600, show_spinner=False)
def load_panel() -> pd.DataFrame | None:
    path = resolve_path("processed") / "panel_pasar_jatim.parquet"
    return pd.read_parquet(path) if path.exists() else None


@st.cache_data(ttl=3600, show_spinner=False)
def load_risk_scores() -> pd.DataFrame | None:
    path = resolve_path("processed") / "risk_scores.parquet"
    return pd.read_parquet(path) if path.exists() else None
