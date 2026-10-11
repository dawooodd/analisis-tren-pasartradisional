"""Agen portal Satu Data Jawa Timur / Open Data Pemda.

Sumber utama indikator aktivitas pasar (jumlah pedagang aktif, retribusi pasar)
yang umumnya tidak dipublikasikan BPS.

Status: nonaktif di settings.yaml sampai endpoint & lisensi data diverifikasi.
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import AgentTask, BaseAgent, FetchResult


class SatuDataAgent(BaseAgent):
    name = "satudata"

    async def fetch(self, task: AgentTask) -> FetchResult:
        raise NotImplementedError("SatuDataAgent.fetch dijadwalkan pada fase pengambilan data")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        raise NotImplementedError("SatuDataAgent.parse dijadwalkan pada fase pengambilan data")
