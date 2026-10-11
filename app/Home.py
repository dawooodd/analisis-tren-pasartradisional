"""Entry point dashboard: `streamlit run app/Home.py` (jalankan dari root proyek)."""

from components.layout import init_page, under_construction  # noqa: I001 (bootstrap sys.path)

init_page("Ringkasan")

import streamlit as st  # noqa: E402

from components.data_access import load_panel  # noqa: E402
from components.sidebar import render_sidebar  # noqa: E402

st.title("Early Warning System Pasar Tradisional Jawa Timur")
st.caption("Evaluasi risiko kebangkrutan & penyusutan pembeli · 38 kab/kota · 2014–2024")

filters = render_sidebar()
panel = load_panel()

if panel is None:
    st.warning("Panel data belum tersedia. Jalankan `make scrape` lalu `make etl`.", icon="📭")
    with st.expander("Filter aktif (debug)"):
        st.json(filters.__dict__)
else:
    under_construction("visualisasi")
