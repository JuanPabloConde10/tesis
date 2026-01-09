import os
from typing import Dict, List

from llm_client.client import Client_llm

MODELOS = [
    {"modelo": "gpt-4o-mini", "provider": "openai"},
    {"modelo": "gpt-4o", "provider": "openai"},
    {"modelo": "gpt-3.5-turbo", "provider": "openai"},
    # Ejemplo de modelo local usando LM Studio (OpenAI-compatible).
    {"modelo": "lmstudio-local", "provider": "local", "base_url": os.getenv("LMSTUDIO_BASE_URL")},
]


def get_models() -> List[str]:
    return [x["modelo"] for x in MODELOS]


def _find_model_entry(modelo: str) -> Dict:
    for entry in MODELOS:
        if entry["modelo"] == modelo:
            return entry
    raise RuntimeError(f"Modelo no habilitado: {modelo}")


def get_client(modelo: str) -> Client_llm:
    entry = _find_model_entry(modelo)
    return Client_llm(
        modelo=entry["modelo"],
        provider=entry["provider"],
        base_url=entry.get("base_url"),
        api_key=entry.get("api_key"),
    )
