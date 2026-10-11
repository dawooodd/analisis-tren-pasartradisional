"""Agen BPS WebAPI — jalur utama pengambilan data.

Endpoint: https://webapi.bps.go.id/v1/api/list/model/data/domain/{kode}/var/{var_id}/key/{KEY}
`domain` = kode wilayah BPS (mis. 3578 = Kota Surabaya).

TODO (fase pengambilan data):
- Pemetaan `indikator` → `var_id` per domain (indicators.yaml > bps_var_id).
- Parsing struktur `datacontent` (kunci gabungan vervar+var+turvar+tahun+turtahun).
"""

from __future__ import annotations

import os
from typing import Any

from agents.base_agent import AgentTask, BaseAgent, FetchResult


class BpsApiAgent(BaseAgent):
    name = "bps_api"

    @property
    def api_key(self) -> str:
        key = os.getenv("BPS_API_KEY", "")
        if not key:
            raise RuntimeError("BPS_API_KEY belum diset di .env")
        return key

    async def fetch(self, task: AgentTask) -> FetchResult:
        raise NotImplementedError("BpsApiAgent.fetch dijadwalkan pada fase pengambilan data")

    def parse(self, payload: FetchResult, task: AgentTask) -> list[dict[str, Any]]:
        raise NotImplementedError("BpsApiAgent.parse dijadwalkan pada fase pengambilan data")
