"""Inisialisasi halaman bersama: sys.path ke root proyek, page config, dan CSS global.

Setiap halaman memanggil `init_page()` sebagai baris pertama setelah import.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_DIR.parent
if str(PROJECT_ROOT) not in sys.path:  # agar `src.*` dapat diimpor tanpa pip install -e
    sys.path.insert(0, str(PROJECT_ROOT))


def init_page(title: str, icon: str = "🏪") -> None:
    st.set_page_config(
        page_title=f"{title} · EWS Pasar Jatim",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    css = APP_DIR / "assets" / "style.css"
    if css.exists():
        st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def under_construction(fase: str) -> None:
    st.info(f"Komponen ini akan diisi pada fase **{fase}**.", icon="🛠️")
