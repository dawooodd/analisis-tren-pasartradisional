"""Halaman: Dampak COVID-19 — Shock magnitude vs. recovery rate."""

from components.layout import init_page, under_construction  # noqa: I001

init_page("Dampak COVID-19", "🦠")

import streamlit as st  # noqa: E402

from components.sidebar import render_sidebar  # noqa: E402

st.title("🦠 Dampak COVID-19")
st.caption("Shock magnitude vs. recovery rate")
filters = render_sidebar()
under_construction("visualisasi")