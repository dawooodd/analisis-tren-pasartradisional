"""Pipeline ETL: raw → interim → processed.

Tahapan (masing-masing fungsi murni DataFrame → DataFrame):
    load_raw_records → deduplicate → flag_outliers → harmonize_units → impute
    → validasi Pandera → to_wide_panel → feature engineering → tulis Parquet
"""

from __future__ import annotations

import logging

from src.ingestion.loaders import load_raw_records
from src.utils.io import setup_logging

log = logging.getLogger("pipeline.etl")


def main() -> int:
    setup_logging()
    raw = load_raw_records()
    log.info("Record mentah dimuat: %d baris", len(raw))
    if raw.empty:
        log.warning("data/raw kosong. Jalankan `make scrape` terlebih dahulu.")
        return 0
    # Tahapan berikut diimplementasikan pada fase ETL:
    # df = deduplicate(raw); df = flag_outliers(df); df = harmonize_units(df)
    # df = impute(df); panel_schema().validate(df); wide = to_wide_panel(df) ...
    raise NotImplementedError("Tahapan transformasi dijadwalkan pada fase ETL")


if __name__ == "__main__":
    raise SystemExit(main())
