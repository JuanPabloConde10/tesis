import os
from typing import List, Optional, TypedDict, TYPE_CHECKING

# importar la factory de manera perezosa (lazy) dentro de get_client para evitar importaciones circulares en tiempo de ejecución
if TYPE_CHECKING:
    from infrastructure.llm_client.client import ClientLLM


class ModelEntry(TypedDict, total=False):
    model: str
    provider: str
    base_url: Optional[str]
    api_key: Optional[str]


MODELS: List[ModelEntry] = [
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


def _find_model_entry(model: str) -> ModelEntry:
    for entry in MODELS:
        if entry["model"] == model:
            return entry
    raise RuntimeError(f"Modelo no habilitado: {model}")


def get_client(modelo: str) -> "ClientLLM":
    entry = _find_model_entry(modelo)
    from infrastructure.llm_client.factory import get_client_for_entry

    return get_client_for_entry(entry)
