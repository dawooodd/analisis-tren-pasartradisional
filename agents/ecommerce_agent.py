"""Agen indikator disrupsi digital.

Cakupan:
- Statistik E-Commerce BPS (tingkat provinsi/kab-kota bila tersedia).
- Google Trends (kata kunci belanja daring/live shopping per wilayah) sebagai proksi bulanan.

Catatan: granularitas beberapa sumber hanya provinsi → ditandai di ETL, bukan dipaksakan ke kab/kota.
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import AgentTask, BaseAgent, FetchResult


class EcommerceAgent(BaseAgent):
    name = "ecommerce"

    async def fetch(self, task: AgentTask) -> FetchResult:
        raise NotImplementedError("EcommerceAgent.fetch dijadwalkan pada fase pengambilan data")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        raise NotImplementedError("EcommerceAgent.parse dijadwalkan pada fase pengambilan data")
