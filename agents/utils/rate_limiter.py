"""Rate limiter asinkron per-host (interval minimum antar-permintaan)."""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict


class HostRateLimiter:
    """Menjamin maksimal `rate_per_s` permintaan per detik untuk setiap host.

    Server BPS kab/kota berbeda host, sehingga pembatasan per-host memungkinkan
    paralelisme antarwilayah tanpa membebani satu server.
    """

    def __init__(self, rate_per_s: float) -> None:
        if rate_per_s <= 0:
            raise ValueError("rate_per_s harus > 0")
        self._interval = 1.0 / rate_per_s
        self._last: dict[str, float] = defaultdict(float)
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def acquire(self, host: str) -> None:
        async with self._locks[host]:
            wait = self._last[host] + self._interval - time.monotonic()
            if wait > 0:
                await asyncio.sleep(wait)
            self._last[host] = time.monotonic()
