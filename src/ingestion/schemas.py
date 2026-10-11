"""Kontrak data (data contract) proyek.

Dua lapis validasi:
1. **Record-level (Pydantic)** — dipakai agen saat `validate()`; menolak baris rusak sedini mungkin.
2. **DataFrame-level (Pandera)** — dipakai pipeline ETL untuk menjamin panel final konsisten.

Format kanonik data adalah **long format**:
    kode_wilayah | tahun | indikator | nilai | satuan | sumber | url_sumber | diambil_pada | is_imputed
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator

TAHUN_MIN, TAHUN_MAX = 2010, 2030  # batas longgar; filter periode analisis di ETL
KODE_PROVINSI = "35"


@dataclass(frozen=True, slots=True)
class Wilayah:
    """Satu kabupaten/kota (dibentuk dari `agents/registry/wilayah_jatim.yaml`)."""

    kode: str
    nama: str
    jenis: Literal["kabupaten", "kota"]
    subdomain: str

    @property
    def label(self) -> str:
        prefix = "Kab." if self.jenis == "kabupaten" else "Kota"
        return f"{prefix} {self.nama}"

    @property
    def bps_url(self) -> str:
        return f"https://{self.subdomain}.bps.go.id"


class RawRecord(BaseModel):
    """Satu observasi indikator untuk satu wilayah pada satu tahun."""

    kode_wilayah: str = Field(pattern=r"^35\d{2}$")
    tahun: int = Field(ge=TAHUN_MIN, le=TAHUN_MAX)
    indikator: str
    nilai: float | None
    satuan: str | None = None
    sumber: str
    url_sumber: str | None = None
    diambil_pada: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_imputed: bool = False

    @field_validator("nilai")
    @classmethod
    def _tolak_tak_hingga(cls, v: float | None) -> float | None:
        if v is not None and v != v:  # NaN -> None agar konsisten
            return None
        if v is not None and abs(v) == float("inf"):
            raise ValueError("nilai tidak boleh infinite")
        return v


def panel_schema():  # pragma: no cover - membutuhkan pandera saat runtime ETL
    """Schema Pandera untuk panel long-format hasil ETL (`data/processed`)."""
    import pandera as pa

    return pa.DataFrameSchema(
        {
            "kode_wilayah": pa.Column(str, pa.Check.str_matches(r"^35\d{2}$")),
            "tahun": pa.Column(int, pa.Check.in_range(TAHUN_MIN, TAHUN_MAX)),
            "indikator": pa.Column(str),
            "nilai": pa.Column(float, nullable=True),
            "sumber": pa.Column(str),
            "is_imputed": pa.Column(bool),
        },
        unique=["kode_wilayah", "tahun", "indikator"],
        coerce=True,
        strict=False,
    )
