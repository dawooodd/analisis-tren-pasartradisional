"""Halaman: E-Commerce vs Pasar — Pertumbuhan e-commerce vs. penurunan lapak fisik."""

from components.layout import init_page, under_construction  # noqa: I001

init_page("E-Commerce vs Pasar", "🛒")

import streamlit as st  # noqa: E402

from components.sidebar import render_sidebar  # noqa: E402

st.title("🛒 E-Commerce vs Pasar")
st.caption("Pertumbuhan e-commerce vs. penurunan lapak fisik")
filters = render_sidebar()
under_construction("visualisasi")