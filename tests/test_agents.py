"""Uji kerangka agen & orchestrator dengan agen palsu (tanpa jaringan)."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from agents.base_agent import AgentTask, BaseAgent, FetchResult, TaskStatus
from agents.orchestrator import Orchestrator, PlannedTask
from agents.utils.rate_limiter import HostRateLimiter
from src.ingestion.schemas import Wilayah

WILAYAH = Wilayah("3578", "Surabaya", "kota", "surabayakota")
TASK = AgentTask(WILAYAH, "jml_penduduk", 2014, 2024)


class OkAgent(BaseAgent):
    name = "ok"

    async def fetch(self, task: AgentTask) -> FetchResult:
        body = [{"tahun": t, "nilai": 1000.0 + t} for t in range(task.tahun_mulai, task.tahun_akhir + 1)]
        return FetchResult(json.dumps(body).encode(), "https://contoh.test/data")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        rows = json.loads(payload.content)
        rows.append({"tahun": 1800, "nilai": 1.0})  # baris invalid → harus dibuang
        return [{"kode_wilayah": task.wilayah.kode, "indikator": task.indikator, **r} for r in rows]


class BrokenAgent(BaseAgent):
    name = "broken"

    async def fetch(self, task: AgentTask) -> FetchResult:
        raise httpx.ConnectError("server down")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        return []


@pytest.fixture
def make_agent(tmp_path):
    def _make(cls):
        return cls(httpx.AsyncClient(), HostRateLimiter(100), tmp_path)
    return _make


async def test_run_sukses_validasi_dan_emit(make_agent, tmp_path):
    res = await make_agent(OkAgent).run(TASK)
    assert res.status is TaskStatus.SUCCESS
    assert len(res.records) == 11 and res.n_invalid == 1
    assert (tmp_path / "ok" / "3578" / "jml_penduduk_2014_2024.records.jsonl").exists()


async def test_run_gagal_terisolasi(make_agent):
    res = await make_agent(BrokenAgent).run(TASK)
    assert res.status is TaskStatus.FAILED
    assert "ConnectError" in res.error


async def test_fallback_chain_ke_agen_kedua(make_agent):
    import asyncio

    orch = Orchestrator(settings={"project": {}, "sources": {}}, agent_classes=(),
                        registry=[], indicators=[])
    agents = {"broken": make_agent(BrokenAgent), "ok": make_agent(OkAgent)}
    res = await orch._run_chain(PlannedTask(TASK, ("broken", "ok")), agents, asyncio.Semaphore(1))
    assert res.status is TaskStatus.SUCCESS and res.agent == "ok"


def test_plan_hanya_sumber_aktif():
    settings = {
        "project": {"tahun_mulai": 2014, "tahun_akhir": 2024},
        "sources": {"ok": {"enabled": True}, "broken": {"enabled": False}},
    }
    registry = [{"kode": "3578", "nama": "Surabaya", "jenis": "kota", "subdomain": "surabayakota"},
                {"kode": "3573", "nama": "Malang", "jenis": "kota", "subdomain": "malangkota"}]
    indicators = [{"kode": "a", "sumber": ["broken", "ok"]}, {"kode": "b", "sumber": ["broken"]}]
    orch = Orchestrator(settings, (OkAgent, BrokenAgent), registry, indicators)

    plan = orch.plan()
    assert len(plan) == 2                      # indikator b dilewati (tidak ada sumber aktif)
    assert all(p.chain == ("ok",) for p in plan)
    assert len(orch.plan(wilayah_filter=["3578"])) == 1
