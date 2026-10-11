"""Market Distress Index (MDI) 0-100 dan klasifikasi zona risiko."""

from __future__ import annotations

import pandas as pd

from src.utils.io import load_settings

KOMPONEN_DEFAULT: dict[str, int] = {
    # kolom fitur : arah risiko (+1 naik = makin berisiko, -1 naik = makin aman)
    "growth_jml_pedagang_aktif": -1,
    "tingkat_kekosongan_kios": +1,
    "growth_retribusi_riil": -1,
    "minimarket_per_10k": +1,
    "recovery_rate": -1,
    "pct_rt_akses_internet": +1,
}


def compute_mdi(panel: pd.DataFrame, komponen: dict[str, int] | None = None,
                bobot: dict[str, float] | None = None) -> pd.Series:
    """Normalisasi min-max per tahun, sesuaikan arah, agregasi tertimbang (default: PCA)."""
    raise NotImplementedError("Dijadwalkan pada fase pemodelan")


def classify_zone(score: float) -> str:
    """Petakan skor MDI ke zona berdasarkan `settings.yaml > risk_index.thresholds`."""
    for zona, (lo, hi) in load_settings()["risk_index"]["thresholds"].items():
        if lo <= score <= hi:
            return zona
    return "tidak_terdefinisi"
