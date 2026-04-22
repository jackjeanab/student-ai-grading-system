from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        requests_per_minute: int,
        protected_paths: tuple[str, ...] = ("/api/submissions",),
    ) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.protected_paths = protected_paths
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if self.requests_per_minute <= 0 or not self._is_protected(request.url.path):
            return await call_next(request)

        client_key = self._client_key(request)
        now = time.monotonic()
        timestamps = self._requests[client_key]
        self._prune_old_requests(timestamps, now)

        if len(timestamps) >= self.requests_per_minute:
            return Response("Rate limit exceeded", status_code=429)

        timestamps.append(now)
        return await call_next(request)

    def _is_protected(self, path: str) -> bool:
        return any(path.startswith(protected_path) for protected_path in self.protected_paths)

    def _client_key(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for", "")
        if forwarded_for:
            return forwarded_for.split(",", maxsplit=1)[0].strip()

        if request.client is None:
            return "unknown"

        return request.client.host

    def _prune_old_requests(self, timestamps: deque[float], now: float) -> None:
        cutoff = now - 60
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()
