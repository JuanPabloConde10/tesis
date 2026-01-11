import os
from typing import Dict, List

from infrastructure.llm_client.factory import get_client_for_entry

MODELS = [
    {"model": "gpt-4o-mini", "provider": "openai"},
    {"model": "gpt-4o", "provider": "openai"},
    {"model": "gpt-3.5-turbo", "provider": "openai"},
    # Ejemplo de modelo local usando LM Studio (OpenAI-compatible).
    {
        "model": "lmstudio-local",
        "provider": "local",
        "base_url": os.getenv("LMSTUDIO_BASE_URL"),
    },
    {"model": "gemini-2.5-flash", "provider": "gemini"},
]


def get_models() -> List[str]:
    return [x["model"] for x in MODELS]


def _find_model_entry(model: str) -> Dict:
    for entry in MODELS:
        if entry["model"] == model:
            return entry
    raise RuntimeError(f"Modelo no habilitado: {model}")


def get_client(modelo: str):
    entry = _find_model_entry(modelo)
    return get_client_for_entry(entry)
