from typing import Optional
import json

from infrastructure.api.global_schemas import StoryRequest
from infrastructure.llm_client import get_client, get_models
from infrastructure.llm_client.models import MODELS
from axis_of_interest.schema_generator import PlotSchemaGenerator
from axis_of_interest.character_assigner import assign_character_names, CharacterNameAssigner
from axis_of_interest.character_attributes import Character, CharacterAttributes
from axis_of_interest.utils import render_plot_schema_md
from axis_of_interest.prompts import template_prompt_generate_cuento
from axis_of_interest.text_gen import generate_text
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
        {
            "id": "3",
            "name": "Modo 3",
            "description": "Seleccionás Axis of Interest y estrategia de interleaving. El Plot Schema se genera automáticamente y se usa para crear el cuento.",
        },
        {
            "id": "4",
            "name": "Modo 4",
            "description": "Seleccionás Axis of Interest y estrategia de interleaving. El Plot Schema se genera automáticamente y se usa para crear el cuento. Además, podés proporcionar atributos de personajes para una asignación más personalizada.",
        },
    ]


def _resolve_model(model_name: Optional[str]) -> str:
    if model_name:
        if model_name not in AVAILABLE_MODELS:
            raise RuntimeError(f"Modelo no habilitado: {model_name}")
        return model_name
    return DEFAULT_MODEL


def _get_provider_for_model(model_name: str) -> Optional[str]:
    """Devuelve el proveedor asociado a un modelo."""
    for entry in MODELS:
        if entry.get("model") == model_name:
            return entry.get("provider")
    return None


def _build_prompts(data: StoryRequest, mode_id: str) -> tuple[str, str]:
    """Construye un prompt simple con los datos del usuario."""
    system_prompt = "Eres un escritor que crea cuentos breves en español, con tono claro y atractivo."
    user_parts = [f"Trama: {data.trama}"]
    if data.genero:
        user_parts.append(f"Género: {data.genero}")
    if data.personajes:
        user_parts.append("Personajes: " + ", ".join(data.personajes))
    if data.experiment_id:
        user_parts.append(f"Identificador de experimento: {data.experiment_id}")
    if mode_id == "0":
       return create_prompt_mode0(data)
    if mode_id == "1":
        return create_prompt_mode1(data)
    user_prompt = "\n".join(user_parts)
    return system_prompt, user_prompt


def _build_characters_section(
    character_names: Optional[list[str]] = None,
    characters: Optional[list[Character]] = None,
) -> str:
    if characters:
        lines = []
        for char in characters:
            desc = f"Descripción: {char.description}. " if char.description else ""
            attrs = (
                f"Valentía {char.attributes.valentia}, "
                f"Bondad {char.attributes.bondad}, "
                f"Astucia {char.attributes.astucia}, "
                f"Maldad {char.attributes.maldad}, "
                f"Carisma {char.attributes.carisma}"
            )
            lines.append(f"- {char.name}. {desc}Atributos: {attrs}.")
        return "\n".join(lines)
    if character_names:
        return "\n".join(f"- {name}" for name in character_names)
    return "No especificado"


def _generate_mode_0(data: StoryRequest, mode_id: str) -> str:
    """Modo 0: Generación directa sin Plot Schema."""
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


def _generate_mode_3(data: StoryRequest) -> tuple[str, dict]:
    """Modo 3: Generación con Plot Schema basado en AOIs seleccionados."""
    if not data.aois or len(data.aois) == 0:
        raise RuntimeError("Modo 3 requiere al menos un Axis of Interest seleccionado")
    
    # Generar Plot Schema
    generator = PlotSchemaGenerator()
    interleaving_strategy = data.interleaving_strategy or "random"
    
    # Si la estrategia es LLM, necesitamos el proveedor, no el modelo
    llm_provider = None
    if interleaving_strategy == "llm":
        model_name = _resolve_model(data.model)
        llm_provider = _get_provider_for_model(model_name)
    
    schema = generator.generate_schema(
        schema_name=f"Historia con {', '.join(data.aois)}",
        aoi_names=data.aois,
        interleaving_strategy=interleaving_strategy,
        llm_provider=llm_provider,
        schema_description=f"Plot schema usando {interleaving_strategy} strategy",
    )
    
    # Asignar personajes
    character_names = data.personajes if data.personajes else ["Personaje A", "Personaje B", "Personaje C"]
    schema_with_names = assign_character_names(
        schema,
        character_names,
        allow_reuse=True,
        seed=42,
    )
    
    # Generar cuento con LLM
    model_name = _resolve_model(data.model)
    client = get_client(model_name)
    
    schema_dict = schema_with_names.model_dump()
    schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)
    
    # Reemplazar placeholder en el prompt
    prompt = template_prompt_generate_cuento.replace("{plot_schema}", schema_json)
    prompt = prompt.replace("{ambiente}", data.trama or "No especificado")
    genero_section = f"Género del cuento: {data.genero}" if data.genero else ""
    prompt = prompt.replace("{genero_section}", genero_section)
    characters_section = _build_characters_section(character_names=character_names)
    prompt = prompt.replace("{characters_section}", characters_section)
    
    print(f"[Modo 3] Longitud del prompt: {len(prompt)} caracteres")
    print(f"[Modo 3] Primeros 500 chars del prompt:\n{prompt[:500]}")
    print(f"[Modo 3] Últimos 500 chars del prompt:\n{prompt[-500:]}")
    
    story = client.generate(
        prompt,
        temperature=data.temperature if data.temperature is not None else 0.7,
        max_tokens=data.max_tokens,  # Solo si el usuario lo especifica
    )
    
    print(f"[Modo 3] Historia generada. Longitud: {len(story)} caracteres")
    print(f"[Modo 3] Primeros 200 chars: {story[:200]}")
    print(f"[Modo 3] Últimos 200 chars: {story[-200:]}")

    return story, schema_with_names.model_dump()




def _generate_mode_4(data: StoryRequest) -> tuple[str, dict]:
    """Modo 4: Generación con Plot Schema y asignación de personajes basada en atributos."""
    if not data.aois or len(data.aois) == 0:
        raise RuntimeError("Modo 4 requiere al menos un Axis of Interest seleccionado")
    
    if not data.character_attributes or len(data.character_attributes) == 0:
        raise RuntimeError("Modo 4 requiere al menos un personaje con atributos")
    
    # Generar Plot Schema
    generator = PlotSchemaGenerator()
    interleaving_strategy = data.interleaving_strategy or "random"
    
    # Si la estrategia es LLM, necesitamos el proveedor
    llm_provider = None
    if interleaving_strategy == "llm":
        model_name = _resolve_model(data.model)
        llm_provider = _get_provider_for_model(model_name)
    
    schema = generator.generate_schema(
        schema_name=f"Historia con {', '.join(data.aois)}",
        aoi_names=data.aois,
        interleaving_strategy=interleaving_strategy,
        llm_provider=llm_provider,
        schema_description=f"Plot schema usando {interleaving_strategy} strategy",
    )
    
    # Convertir personajes del request a objetos Character
    characters = [
        Character(
            name=char.name,
            attributes=CharacterAttributes(
                valentia=char.attributes.valentia,
                bondad=char.attributes.bondad,
                astucia=char.attributes.astucia,
                maldad=char.attributes.maldad,
                carisma=char.attributes.carisma,
            ),
            description=char.description,
        )
        for char in data.character_attributes
    ]
    
    # Asignar personajes basándose en atributos
    assigner = CharacterNameAssigner(seed=42)
    schema_with_names = assigner.assign_names_by_attributes(
        schema,
        characters,
        allow_reuse=True,
    )
    
    # Generar cuento con LLM
    model_name = _resolve_model(data.model)
    client = get_client(model_name)
    
    schema_dict = schema_with_names.model_dump()
    schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)
    
    # Reemplazar placeholder en el prompt
    prompt = template_prompt_generate_cuento.replace("{plot_schema}", schema_json)
    prompt = prompt.replace("{ambiente}", data.trama or "No especificado")
    genero_section = f"Género del cuento: {data.genero}" if data.genero else ""
    prompt = prompt.replace("{genero_section}", genero_section)
    characters_section = _build_characters_section(characters=characters)
    prompt = prompt.replace("{characters_section}", characters_section)
    
    print(f"[Modo 4] Longitud del prompt: {len(prompt)} caracteres")
    print(f"[Modo 4] Primeros 500 chars del prompt:\n{prompt[:500]}")
    print(f"[Modo 4] Últimos 500 chars del prompt:\n{prompt[-500:]}")
    
    story = client.generate(
        prompt,
        temperature=data.temperature if data.temperature is not None else 0.7,
        max_tokens=data.max_tokens,
    )
    
    print(f"[Modo 4] Historia generada. Longitud: {len(story)} caracteres")
    print(f"[Modo 4] Primeros 200 chars: {story[:200]}")
    print(f"[Modo 4] Últimos 200 chars: {story[-200:]}")

    return story, schema_with_names.model_dump()


def generate_the_story(data: StoryRequest) -> str | tuple[str, dict]:
    """Genera un cuento según el modo seleccionado."""
    mode_id = data.mode or "0"
    
    if mode_id == "0":
        return _generate_mode_0(data)
    elif mode_id == "1":
        # TODO: Implementar modo 1
        return _generate_mode_0(data)
    elif mode_id == "2":
        # TODO: Implementar modo 2
        return _generate_mode_0(data)
    elif mode_id == "3":
        return _generate_mode_3(data)
    elif mode_id == "4":
        return _generate_mode_4(data)
    else:
        # Fallback a modo 0
        return _generate_mode_0(data)
