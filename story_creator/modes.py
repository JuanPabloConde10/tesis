from typing import Optional

from infrastructure.api.global_schemas import StoryRequest
from infrastructure.llm_client import get_client, get_models

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


def _build_prompts(data: StoryRequest) -> tuple[str, str]:
    """Construye un prompt simple con los datos del usuario."""
    system_prompt = "Eres un escritor que crea cuentos breves en español, con tono claro y atractivo."
    user_parts = [f"Trama: {data.trama}"]
    if data.genero:
        user_parts.append(f"Género: {data.genero}")
    if data.arco:
        user_parts.append(f"Arco narrativo: {data.arco}")
    if data.personajes:
        user_parts.append("Personajes: " + ", ".join(data.personajes))
    if data.experiment_id:
        user_parts.append(f"Identificador de experimento: {data.experiment_id}")
    user_prompt = "\n".join(user_parts)
    return system_prompt, user_prompt


def generate_the_story(data: StoryRequest) -> str:
    model_name = _resolve_model(data.model)
    client = get_client(model_name)
    system_prompt, user_prompt = _build_prompts(data)
    return client.generate(
        user_prompt,
        system_prompt=system_prompt,
        temperature=data.temperature if data.temperature is not None else 0.7,
        max_tokens=data.max_tokens,
    )
