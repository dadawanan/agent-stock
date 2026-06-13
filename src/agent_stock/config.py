from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv() -> None:
    """Load .env file if present."""
    for env_path in [Path.cwd() / ".env", Path(__file__).resolve().parents[3] / ".env"]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
            break


_load_dotenv()


class Settings:
    """Lazy-loaded settings from environment variables."""

    def __init__(self) -> None:
        self._cache: dict[str, object] = {}

    def _get(self, key: str, loader) -> object:
        if key not in self._cache:
            self._cache[key] = loader()
        return self._cache[key]

    @property
    def openai_api_key(self) -> str:
        return self._get("openai_api_key", lambda: os.environ.get("OPENAI_API_KEY", ""))  # type: ignore[return-value]

    @property
    def stock_api_url(self) -> str:
        return self._get("stock_api_url", lambda: os.environ.get("STOCK_API_URL", "http://localhost:8000"))  # type: ignore[return-value]

    @property
    def agent_host(self) -> str:
        return self._get("agent_host", lambda: os.environ.get("AGENT_HOST", "0.0.0.0"))  # type: ignore[return-value]

    @property
    def agent_port(self) -> int:
        return self._get("agent_port", lambda: int(os.environ.get("AGENT_PORT", "8001")))  # type: ignore[return-value]


settings = Settings()
