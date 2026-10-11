"""Halaman: Tren Time-Series — Tren indikator per kab/kota."""

from components.layout import init_page, under_construction  # noqa: I001

init_page("Tren Time-Series", "📈")

import streamlit as st  # noqa: E402

from components.sidebar import render_sidebar  # noqa: E402

st.title("📈 Tren Time-Series")
st.caption("Tren indikator per kab/kota")
filters = render_sidebar()
under_construction("visualisasi")