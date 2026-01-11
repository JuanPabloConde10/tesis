"""Factory para crear clientes LLM.

Esta fábrica centraliza la creación de clientes LLM.
Cada cliente se configura según la entrada del modelo
"""

import os
from typing import Optional, cast, TYPE_CHECKING

if TYPE_CHECKING:
    # Import for type checking only to avoid circular runtime import
    from .models import ModelEntry

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


def get_client_for_entry(entry: "ModelEntry") -> ClientLLM:
    return resolve_client(
        entry["provider"],
        entry["model"],
        base_url=entry.get("base_url"),
        api_key=entry.get("api_key"),
    )


