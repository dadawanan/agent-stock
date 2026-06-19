from __future__ import annotations

from contextvars import ContextVar

# Per-request auth token, set in main.py from the incoming Authorization header.
auth_token: ContextVar[str] = ContextVar("auth_token", default="")
