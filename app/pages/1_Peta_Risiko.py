"""Halaman: Peta Risiko — Choropleth 38 kab/kota + klaster LISA."""

from components.layout import init_page, under_construction  # noqa: I001

init_page("Peta Risiko", "🗺️")

import streamlit as st  # noqa: E402

from components.sidebar import render_sidebar  # noqa: E402

st.title("🗺️ Peta Risiko")
st.caption("Choropleth 38 kab/kota + klaster LISA")
filters = render_sidebar()
under_construction("visualisasi")