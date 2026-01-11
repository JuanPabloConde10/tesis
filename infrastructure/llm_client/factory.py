"""Factory to resolve and instantiate LLM clients/providers.

This is a thin wrapper that uses the existing `ClientLLM` facade
implemented in `client.py` to preserve current behaviour while
providing a central place to construct clients.
"""

import os
from typing import Optional, cast

from .client import ClientLLM, ProviderName


def resolve_client(
    provider: str,
    model: str,
    *,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ClientLLM:
    normalized_raw = provider.lower()
    if normalized_raw not in ("openai", "gemini", "local"):
        raise ValueError(f"Proveedor no soportado: {provider}")
    normalized = cast(ProviderName, normalized_raw)

    key = api_key
    if not key:
        if normalized == "openai":
            key = os.getenv("OPENAI_API_KEY")
        elif normalized == "gemini":
            key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif normalized == "local":
            key = os.getenv("LMSTUDIO_API_KEY") or os.getenv("LOCAL_LLM_API_KEY")

    return ClientLLM(provider=normalized, model=model, api_key=key, base_url=base_url)


def get_client_for_entry(entry: dict) -> ClientLLM:
    return resolve_client(
        entry["provider"],
        entry["model"],
        base_url=entry.get("base_url"),
        api_key=entry.get("api_key"),
    )


