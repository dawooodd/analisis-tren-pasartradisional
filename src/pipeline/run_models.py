"""Pipeline pemodelan: processed panel → ITS, forecast, spasial, MDI → data/processed/*.parquet."""

from __future__ import annotations

import logging

from src.utils.io import resolve_path, setup_logging

log = logging.getLogger("pipeline.models")


def main() -> int:
    setup_logging()
    panel_path = resolve_path("processed") / "panel_pasar_jatim.parquet"
    if not panel_path.exists():
        log.warning("Panel belum tersedia (%s). Jalankan `make etl`.", panel_path)
        return 0
    raise NotImplementedError("Pipeline pemodelan dijadwalkan pada fase pemodelan")


if __name__ == "__main__":
    raise SystemExit(main())
