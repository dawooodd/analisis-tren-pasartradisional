"""Sidebar filter global. State disimpan di `st.session_state` dan disinkronkan ke URL."""

from __future__ import annotations

from dataclasses import dataclass, field

import streamlit as st

from src.utils.io import load_registry, load_settings

METRIK: dict[str, str] = {
    "jml_pasar_tradisional": "Jumlah pasar tradisional",
    "jml_pedagang_aktif": "Jumlah pedagang aktif",
    "kepadatan_lapak_10k": "Kepadatan lapak per 10.000 penduduk",
    "laju_penutupan": "Laju penutupan pasar (%)",
    "mdi": "Market Distress Index",
    "recovery_rate": "Recovery rate pasca-COVID",
}
PRESET_PERIODE: dict[str, tuple[int, int]] = {
    "Seluruh periode": (2014, 2024),
    "Pra-COVID": (2014, 2019),
    "COVID": (2020, 2021),
    "Pasca-COVID": (2022, 2024),
}


@dataclass
class FilterState:
    tahun: tuple[int, int]
    wilayah: list[str] = field(default_factory=list)  # kode BPS; kosong = semua
    jenis: str = "Semua"
    metrik: str = "jml_pasar_tradisional"
    mode_yoy: bool = False
    skenario: str = "baseline"


def render_sidebar() -> FilterState:
    proj = load_settings()["project"]
    registry = load_registry()
    label = {w["kode"]: ("Kab. " if w["jenis"] == "kabupaten" else "Kota ") + w["nama"]
             for w in registry}

    with st.sidebar:
        st.header("Filter")
        preset = st.selectbox("Periode cepat", list(PRESET_PERIODE), key="f_preset")
        tahun = st.slider("Rentang tahun", proj["tahun_mulai"], proj["tahun_akhir"],
                          PRESET_PERIODE[preset], key=f"f_tahun_{preset}")
        jenis = st.radio("Jenis wilayah", ["Semua", "Kabupaten", "Kota"],
                         horizontal=True, key="f_jenis")
        opsi = [k for k, w in zip(label, registry, strict=True)
                if jenis == "Semua" or w["jenis"] == jenis.lower()]
        wilayah = st.multiselect("Kabupaten/Kota", opsi, format_func=label.get,
                                 placeholder="Semua Jawa Timur", key="f_wilayah")
        metrik = st.selectbox("Metrik", list(METRIK), format_func=METRIK.get, key="f_metrik")
        mode_yoy = st.toggle("Tampilkan pertumbuhan YoY (%)", key="f_yoy")
        skenario = st.selectbox("Skenario proyeksi",
                                ["baseline", "akselerasi_digital", "intervensi_kebijakan"],
                                key="f_skenario")

    return FilterState(tuple(tahun), wilayah, jenis, metrik, mode_yoy, skenario)
