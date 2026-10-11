"""Kebijakan retry untuk error jaringan yang bersifat sementara."""

from __future__ import annotations

import httpx
from tenacity import (
    AsyncRetrying,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def is_transient(exc: BaseException) -> bool:
    """True bila error layak dicoba ulang (timeout, koneksi putus, 429/5xx)."""
    if isinstance(exc, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return False


def retrying(max_attempts: int, backoff_min_s: float, backoff_max_s: float) -> AsyncRetrying:
    """Factory `AsyncRetrying` dengan exponential backoff + jitter.

    Contoh:
        async for attempt in retrying(4, 1, 30):
            with attempt:
                resp = await client.get(url)
                resp.raise_for_status()
    """
    return AsyncRetrying(
        retry=retry_if_exception(is_transient),
        stop=stop_after_attempt(max_attempts),
        wait=wait_random_exponential(min=backoff_min_s, max=backoff_max_s),
        reraise=True,
    )
