"""Halaman: Proyeksi 2029 — Fan chart proyeksi & ranking risiko 2029."""

from components.layout import init_page, under_construction  # noqa: I001

init_page("Proyeksi 2029", "🔮")

import streamlit as st  # noqa: E402

from components.sidebar import render_sidebar  # noqa: E402

st.title("🔮 Proyeksi 2029")
st.caption("Fan chart proyeksi & ranking risiko 2029")
filters = render_sidebar()
under_construction("visualisasi")