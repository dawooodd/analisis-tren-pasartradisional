"""Kerangka dasar agen pengumpul data.

Setiap agen mengikuti siklus Template Method:

    fetch  →  parse  →  validate  →  emit
    (I/O)    (murni)   (kontrak)    (persist raw)

Subkelas cukup mengimplementasikan `fetch()` dan `parse()`. Penanganan error,
rate limiting, retry, validasi, dan penyimpanan raw sudah ditangani di sini
sehingga kegagalan satu wilayah/indikator tidak menghentikan pipeline.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar
from urllib.parse import urlparse

import httpx
from pydantic import ValidationError

from agents.utils.rate_limiter import HostRateLimiter
from agents.utils.retry import retrying
from src.ingestion.schemas import RawRecord, Wilayah


class TaskStatus(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"            # berhasil diakses tetapi tidak ada baris valid
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AgentTask:
    """Unit kerja: satu indikator untuk satu wilayah pada rentang tahun."""

    wilayah: Wilayah
    indikator: str
    tahun_mulai: int
    tahun_akhir: int

    @property
    def key(self) -> str:
        return f"{self.wilayah.kode}:{self.indikator}:{self.tahun_mulai}-{self.tahun_akhir}"


@dataclass(slots=True)
class FetchResult:
    """Payload mentah hasil `fetch()` (disimpan apa adanya untuk audit & reproduksibilitas)."""

    content: bytes
    url: str
    content_type: str = "application/json"

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content).hexdigest()

    @property
    def extension(self) -> str:
        if "json" in self.content_type:
            return "json"
        if "html" in self.content_type:
            return "html"
        if "csv" in self.content_type:
            return "csv"
        return "bin"


@dataclass(slots=True)
class AgentResult:
    task: AgentTask
    agent: str
    status: TaskStatus
    records: list[RawRecord] = field(default_factory=list, repr=False)
    n_invalid: int = 0
    error: str | None = None
    durasi_s: float = 0.0
    raw_path: str | None = None

    def summary(self) -> dict[str, Any]:
        return {
            "key": self.task.key,
            "agent": self.agent,
            "status": self.status.value,
            "n_records": len(self.records),
            "n_invalid": self.n_invalid,
            "error": self.error,
            "durasi_s": round(self.durasi_s, 3),
            "raw_path": self.raw_path,
        }


@dataclass(frozen=True, slots=True)
class RetryConfig:
    max_attempts: int = 4
    backoff_min_s: float = 1.0
    backoff_max_s: float = 30.0


class BaseAgent(ABC):
    """Kelas abstrak seluruh agen. `name` harus sama dengan key di `settings.yaml > sources`."""

    name: ClassVar[str]

    def __init__(
        self,
        client: httpx.AsyncClient,
        limiter: HostRateLimiter,
        raw_dir: Path,
        retry_cfg: RetryConfig | None = None,
    ) -> None:
        self.client = client
        self.limiter = limiter
        self.raw_dir = raw_dir
        self.retry_cfg = retry_cfg or RetryConfig()
        self.log = logging.getLogger(f"agents.{self.name}")

    # ------------------------------------------------------------------ #
    # Kontrak yang wajib diimplementasikan subkelas
    # ------------------------------------------------------------------ #
    @abstractmethod
    async def fetch(self, task: AgentTask) -> FetchResult:
        """Ambil payload mentah dari sumber. Gunakan `self._get()` untuk HTTP."""

    @abstractmethod
    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        """Ubah payload mentah menjadi list dict ber-field `RawRecord`. Harus fungsi murni."""

    # ------------------------------------------------------------------ #
    # Hook default (boleh di-override)
    # ------------------------------------------------------------------ #
    def validate(self, rows: list[dict[str, Any]]) -> tuple[list[RawRecord], int]:
        valid: list[RawRecord] = []
        invalid = 0
        for row in rows:
            row.setdefault("sumber", self.name)
            try:
                valid.append(RawRecord.model_validate(row))
            except ValidationError as exc:
                invalid += 1
                self.log.debug("Baris tidak valid %s: %s", row, exc.errors()[:1])
        return valid, invalid

    def emit(self, payload: FetchResult, records: list[RawRecord], task: AgentTask) -> Path:
        """Simpan payload + record ke `data/raw/{agent}/{kode}/`. Idempoten berbasis hash."""
        out_dir = self.raw_dir / self.name / task.wilayah.kode
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = f"{task.indikator}_{task.tahun_mulai}_{task.tahun_akhir}"
        meta_path = out_dir / f"{stem}.meta.json"

        if meta_path.exists():
            old = json.loads(meta_path.read_text(encoding="utf-8"))
            if old.get("sha256") == payload.sha256:
                self.log.debug("Payload tidak berubah, skip tulis: %s", task.key)
                return meta_path

        (out_dir / f"{stem}.{payload.extension}").write_bytes(payload.content)
        with (out_dir / f"{stem}.records.jsonl").open("w", encoding="utf-8") as f:
            for r in records:
                f.write(r.model_dump_json() + "\n")
        meta_path.write_text(
            json.dumps(
                {"task": task.key, "url": payload.url, "sha256": payload.sha256,
                 "n_records": len(records)},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return meta_path

    # ------------------------------------------------------------------ #
    # Helper HTTP: rate limit per-host + retry
    # ------------------------------------------------------------------ #
    async def _get(self, url: str, **kwargs: Any) -> httpx.Response:
        host = urlparse(url).netloc
        cfg = self.retry_cfg
        async for attempt in retrying(cfg.max_attempts, cfg.backoff_min_s, cfg.backoff_max_s):
            with attempt:
                await self.limiter.acquire(host)
                resp = await self.client.get(url, **kwargs)
                resp.raise_for_status()
                return resp
        raise RuntimeError("unreachable")  # pragma: no cover

    # ------------------------------------------------------------------ #
    # Template method
    # ------------------------------------------------------------------ #
    async def run(self, task: AgentTask) -> AgentResult:
        t0 = time.perf_counter()
        try:
            payload = await self.fetch(task)
            rows = self.parse(payload, task)
            records, n_invalid = self.validate(rows)
            raw_path = self.emit(payload, records, task)
            status = TaskStatus.SUCCESS if records else TaskStatus.EMPTY
            return AgentResult(task, self.name, status, records, n_invalid,
                               durasi_s=time.perf_counter() - t0, raw_path=str(raw_path))
        except Exception as exc:  # isolasi kegagalan: jangan hentikan pipeline
            self.log.warning("Gagal %s: %s: %s", task.key, type(exc).__name__, exc)
            return AgentResult(task, self.name, TaskStatus.FAILED,
                               error=f"{type(exc).__name__}: {exc}",
                               durasi_s=time.perf_counter() - t0)
