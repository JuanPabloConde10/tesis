from typing import Optional

from infrastructure.api.global_schemas import StoryRequest
from infrastructure.llm_client import get_client, get_models
from story_creator.mode0 import create_prompt_mode0
from story_creator.mode1 import create_prompt_mode1
from story_creator.mode2 import generate_story_mode2

AVAILABLE_MODELS = get_models()
DEFAULT_MODEL = AVAILABLE_MODELS[0]


def get_modes() -> list:
    return [
        {"id": "0", "name": "Modo 0", "description": "Generación a pelo."},
        {
            "id": "1",
            "name": "Modo 1",
            "description": "Utilizando el Plot Schema en el prompt",
        },
        {
            "id": "2",
            "name": "Modo 2",
            "description": "Creamos el Plot Schema y chunks para cada escena. Luego le pedimos al LLM que hile estas escenas en un unico cuento",
        },
    ]


def _resolve_model(model_name: Optional[str]) -> str:
    if model_name:
        if model_name not in AVAILABLE_MODELS:
            raise RuntimeError(f"Modelo no habilitado: {model_name}")
        return model_name
    return DEFAULT_MODEL


def _build_prompts(data: StoryRequest, mode_id: str) -> tuple[str, str]:
    """Construye un prompt dependiendo del modo."""
    if mode_id == "0":
        return create_prompt_mode0(data)
    if mode_id == "1":
        return create_prompt_mode1(data)
    raise RuntimeError(f"Modo de creación no implementado: {mode_id}")


def generate_the_story(data: StoryRequest, mode_id: str) -> str:
    model_name = _resolve_model(data.model)
    client = get_client(model_name)
    temperature = data.temperature if data.temperature is not None else 0.7

    if mode_id == "2":
        return generate_story_mode2(
            data,
            client,
            temperature=temperature,
            max_tokens=data.max_tokens,
            seed=42,
        )

    system_prompt, user_prompt = _build_prompts(data, mode_id)
    return client.generate(
        user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=data.max_tokens,
    )
