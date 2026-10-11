"""Orchestrator multi-agen asinkron.

Alur:
1. Muat registry 38 kab/kota + kamus indikator.
2. Bentuk task (wilayah × indikator) beserta *fallback chain* agen
   sesuai urutan `sumber` pada `config/indicators.yaml` (hanya sumber yang `enabled`).
3. Eksekusi konkuren dengan `asyncio.Semaphore` (batas `agents.max_concurrency`).
4. Untuk tiap task: coba agen pertama; bila FAILED/EMPTY, lanjut ke agen berikutnya.
5. Tulis manifest run ke `logs/` untuk audit & resume.

CLI:
    python -m agents.orchestrator                      # semua wilayah & indikator
    python -m agents.orchestrator --wilayah 3578 3573  # subset wilayah
    python -m agents.orchestrator --indikator jml_penduduk --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

from agents.base_agent import AgentResult, AgentTask, BaseAgent, RetryConfig, TaskStatus
from agents.bps_api_agent import BpsApiAgent
from agents.bps_html_agent import BpsHtmlAgent
from agents.ecommerce_agent import EcommerceAgent
from agents.satudata_agent import SatuDataAgent
from agents.utils.rate_limiter import HostRateLimiter
from agents.utils.user_agent import default_headers
from src.ingestion.schemas import Wilayah
from src.utils.io import load_indicators, load_registry, load_settings, resolve_path, setup_logging

log = logging.getLogger("agents.orchestrator")

DEFAULT_AGENTS: tuple[type[BaseAgent], ...] = (
    BpsApiAgent,
    BpsHtmlAgent,
    SatuDataAgent,
    EcommerceAgent,
)


@dataclass(frozen=True, slots=True)
class PlannedTask:
    task: AgentTask
    chain: tuple[str, ...]  # nama agen berurutan (primer → fallback)


class Orchestrator:
    def __init__(
        self,
        settings: dict[str, Any] | None = None,
        agent_classes: Iterable[type[BaseAgent]] = DEFAULT_AGENTS,
        registry: list[dict[str, Any]] | None = None,
        indicators: list[dict[str, Any]] | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.agent_classes = {cls.name: cls for cls in agent_classes}
        self.registry = registry if registry is not None else load_registry()
        self.indicators = indicators if indicators is not None else load_indicators()

    # ------------------------------------------------------------------ #
    # Perencanaan
    # ------------------------------------------------------------------ #
    def _enabled_sources(self) -> set[str]:
        sources = self.settings.get("sources", {})
        return {
            name for name in self.agent_classes
            if sources.get(name, {}).get("enabled", True)
        }

    def plan(
        self,
        wilayah_filter: Sequence[str] | None = None,
        indikator_filter: Sequence[str] | None = None,
    ) -> list[PlannedTask]:
        proj = self.settings["project"]
        enabled = self._enabled_sources()
        wilayah = [Wilayah(**w) for w in self.registry
                   if not wilayah_filter or w["kode"] in wilayah_filter]

        planned: list[PlannedTask] = []
        for ind in self.indicators:
            if indikator_filter and ind["kode"] not in indikator_filter:
                continue
            chain = tuple(s for s in ind.get("sumber", []) if s in enabled)
            if not chain:
                log.info("Indikator %s dilewati: tidak ada sumber aktif", ind["kode"])
                continue
            for w in wilayah:
                task = AgentTask(w, ind["kode"], proj["tahun_mulai"], proj["tahun_akhir"])
                planned.append(PlannedTask(task, chain))
        return planned

    # ------------------------------------------------------------------ #
    # Eksekusi
    # ------------------------------------------------------------------ #
    async def _run_chain(
        self, pt: PlannedTask, agents: dict[str, BaseAgent], sem: asyncio.Semaphore
    ) -> AgentResult:
        async with sem:
            result: AgentResult | None = None
            for name in pt.chain:
                result = await agents[name].run(pt.task)
                if result.status is TaskStatus.SUCCESS:
                    return result
                log.debug("Fallback %s: %s → agen berikutnya", pt.task.key, name)
            assert result is not None
            return result

    def _build_agents(self, client: httpx.AsyncClient) -> dict[str, BaseAgent]:
        cfg = self.settings["agents"]
        limiter = HostRateLimiter(cfg["rate_limit_per_s"])
        retry_cfg = RetryConfig(
            max_attempts=cfg["retry"]["max_attempts"],
            backoff_min_s=cfg["retry"]["backoff_min_s"],
            backoff_max_s=cfg["retry"]["backoff_max_s"],
        )
        raw_dir = resolve_path("raw")
        return {
            name: cls(client, limiter, raw_dir, retry_cfg)
            for name, cls in self.agent_classes.items()
        }

    async def run(self, planned: list[PlannedTask]) -> list[AgentResult]:
        cfg = self.settings["agents"]
        sem = asyncio.Semaphore(cfg["max_concurrency"])
        async with httpx.AsyncClient(
            headers=default_headers(),
            timeout=cfg["request_timeout_s"],
            follow_redirects=True,
        ) as client:
            agents = self._build_agents(client)
            return await asyncio.gather(*(self._run_chain(pt, agents, sem) for pt in planned))

    # ------------------------------------------------------------------ #
    # Pelaporan
    # ------------------------------------------------------------------ #
    @staticmethod
    def write_manifest(results: list[AgentResult], out_dir: Path) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = out_dir / f"run_manifest_{ts}.json"
        counts = Counter(r.status.value for r in results)
        path.write_text(
            json.dumps(
                {"timestamp": ts, "total": len(results), "status": dict(counts),
                 "results": [r.summary() for r in results]},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Orchestrator agen data pasar Jatim")
    parser.add_argument("--wilayah", nargs="*", help="Filter kode wilayah BPS, mis. 3578")
    parser.add_argument("--indikator", nargs="*", help="Filter kode indikator")
    parser.add_argument("--dry-run", action="store_true", help="Tampilkan rencana tanpa eksekusi")
    args = parser.parse_args(argv)

    setup_logging()
    orch = Orchestrator()
    planned = orch.plan(args.wilayah, args.indikator)
    log.info("Rencana: %d task", len(planned))

    if args.dry_run:
        for pt in planned[:20]:
            log.info("  %s  via %s", pt.task.key, " -> ".join(pt.chain))
        if len(planned) > 20:
            log.info("  ... (+%d task)", len(planned) - 20)
        return 0

    results = asyncio.run(orch.run(planned))
    manifest = orch.write_manifest(results, resolve_path("logs"))
    log.info("Selesai: %s | manifest: %s",
             dict(Counter(r.status.value for r in results)), manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
