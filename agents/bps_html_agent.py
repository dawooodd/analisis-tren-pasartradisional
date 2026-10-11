"""Agen fallback: scraping tabel HTML dinamis situs BPS kab/kota.

Dipakai hanya bila indikator tidak tersedia di WebAPI (mis. publikasi "Kabupaten Dalam Angka").
Target URL: https://{subdomain}.bps.go.id/statistics-table/...

TODO (fase pengambilan data):
- Tentukan apakah tabel dirender server-side (selectolax cukup) atau client-side (Playwright).
- Normalisasi header tabel multi-baris & angka format Indonesia ("1.234,5").
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import AgentTask, BaseAgent, FetchResult


class BpsHtmlAgent(BaseAgent):
    name = "bps_html"

    async def fetch(self, task: AgentTask) -> FetchResult:
        raise NotImplementedError("BpsHtmlAgent.fetch dijadwalkan pada fase pengambilan data")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        raise NotImplementedError("BpsHtmlAgent.parse dijadwalkan pada fase pengambilan data")
