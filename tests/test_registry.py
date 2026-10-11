"""Validasi registry & konfigurasi (offline)."""

from collections import Counter

from src.utils.io import load_indicators, load_registry, load_settings


def test_registry_38_wilayah():
    reg = load_registry()
    assert len(reg) == 38
    assert Counter(w["jenis"] for w in reg) == {"kabupaten": 29, "kota": 9}


def test_registry_kode_unik_dan_valid():
    reg = load_registry()
    kode = [w["kode"] for w in reg]
    assert len(set(kode)) == 38
    assert all(k.startswith("35") and len(k) == 4 for k in kode)
    assert len({w["subdomain"] for w in reg}) == 38


def test_sumber_indikator_terdaftar_di_settings():
    sources = set(load_settings()["sources"])
    for ind in load_indicators():
        assert set(ind["sumber"]) <= sources, ind["kode"]


def test_indikator_unik():
    kode = [i["kode"] for i in load_indicators()]
    assert len(kode) == len(set(kode))
