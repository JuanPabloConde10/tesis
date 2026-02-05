"""
Modo 2: Plot Schema + chunks por escena → LLM hila un único cuento.

Integra axis_of_interest (PlotSchemaGenerator, assign_character_names,
generate_text, prompt gramática) y devuelve el cuento generado por el LLM.
"""

from typing import List, Optional, Any

from infrastructure.api.global_schemas import StoryRequest
from axis_of_interest.registry import list_of_aoi
from axis_of_interest.schema_generator import create_plot_schema
from axis_of_interest.character_assigner import assign_character_names
from axis_of_interest.text_gen import generate_text
from axis_of_interest.prompts import (
    template_prompt_generate_cuento_gramatica,
    template_prompt_generate_cuento,
)
import json


def _default_aoi_names() -> List[str]:
    names = [aoi.name for aoi in list_of_aoi]
    if len(names) >= 2:
        return names[:2]
    return names[:1] if names else []

def _schema_description(data: StoryRequest) -> str:
    parts = [f"Trama: {data.trama}"]
    if data.genero:
        parts.append(f"Género: {data.genero}")
    if data.arco:
        parts.append(f"Arco: {data.arco}")
    if data.experiment_id:
        parts.append(f"Experimento: {data.experiment_id}")
    return " | ".join(parts)


def generate_story_mode2(
    data: StoryRequest,
    client: Any,
    *,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    seed: int = 42,
) -> str:
    """
    Genera un cuento con el flujo Modo 2:
    1. Plot Schema a partir de AOIs y estrategia.
    2. Asignación de nombres a personajes.
    3. Según el método elegido:
       - gramatica: Genera texto simple con gramática, luego LLM lo transforma
       - aoi_directo: Envía el Plot Schema completo (JSON) al LLM

    Usa el mismo `client` (ClientLLM) que el resto de modos.
    """
    aoi_names = data.aoi_names if data.aoi_names else _default_aoi_names()
    if not aoi_names:
        raise RuntimeError(
            "Modo 2 requiere al menos un Axis of Interest. "
            "Seleccioná AOIs en el formulario o configurá axis_of_interest."
        )

    strategy = (data.strategy or "sequential").strip().lower()
    allowed = ("sequential", "round_robin", "parallel", "random")
    if strategy not in allowed:
        strategy = "sequential"

    personajes = data.personajes if data.personajes else ["Protagonista"]
    schema_name = "Story"
    schema_description = _schema_description(data)

    schema = create_plot_schema(
        schema_name,
        aoi_names,
        strategy=strategy,
        description=schema_description,
    )
    schema_with_names = assign_character_names(
        schema,
        personajes,
        allow_reuse=True,
        seed=seed,
    )

    # Elegir método de generación: gramática o AOI directo
    generation_method = (data.generation_method or "gramatica").strip().lower()
    if generation_method not in ("gramatica", "aoi_directo"):
        generation_method = "gramatica"

    if generation_method == "gramatica":
        # Método 1: Gramática (texto simple → LLM transforma)
        simple_text = generate_text(schema_with_names)
        prompt = template_prompt_generate_cuento_gramatica.replace(
            "{texto_gramatica}", simple_text
        )
    else:
        # Método 2: AOI directo (schema JSON → LLM genera)
        schema_dict = schema_with_names.model_dump()
        schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)
        prompt = template_prompt_generate_cuento.replace(
            "{plot_schema}", schema_json
        )

    return client.generate(
        prompt,
        system_prompt=None,
        temperature=temperature,
        max_tokens=max_tokens,
    )
