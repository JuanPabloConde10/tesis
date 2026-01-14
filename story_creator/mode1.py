import json
from typing import List, Optional

from infrastructure.api.global_schemas import StoryRequest
from infrastructure.llm_client import get_client, get_models
from axis_of_interest.schema_generator import create_plot_schema
from axis_of_interest.registry import list_of_aoi
from axis_of_interest.prompts import (
    tenplate_prompt_generar_axis_of_interest,
    template_prompt_generate_cuento,
)
from axis_of_interest.character_assigner import assign_character_names


def create_prompt_mode1(data: StoryRequest) -> tuple[str, str]:
    system_prompt = "Eres un escritor que crea cuentos breves en español, con tono claro y atractivo."
    if data.aoi_names:
        aoi_list = data.aoi_names
    else:
        aoi_list = get_bests_aoi(data)
    strategy = data.strategy or "sequential"
    schema_description = _build_schema_description(data)
    plot_schema = create_plot_schema(
        "Peñarol", aoi_list, strategy, schema_description
    )
    if data.personajes:
        plot_schema = assign_character_names(plot_schema, data.personajes, allow_reuse=True)
    plot_schema_json = json.dumps(
        plot_schema.model_dump(), indent=2, ensure_ascii=False
    )
    user_prompt = template_prompt_generate_cuento.replace(
        "{plot_schema}", plot_schema_json
    )

    return system_prompt, user_prompt


def get_bests_aoi(data: StoryRequest) -> List[str]:
    available_names = [aoi.name for aoi in list_of_aoi]
    if not available_names:
        return []

    prompt = tenplate_prompt_generar_axis_of_interest.replace(
        "{data}", json.dumps(_build_story_payload(data), ensure_ascii=False)
    ).replace(
        "{axis_of_interest}",
        json.dumps([aoi.model_dump() for aoi in list_of_aoi], indent=2, ensure_ascii=False),
    )

    model_name = _resolve_model_name(data.model)
    client = get_client(model_name)
    try:
        response = client.generate(prompt)
    except Exception:
        return available_names[:2]

    names = _parse_aoi_response(response, available_names)
    return names or available_names[:2]


def _resolve_model_name(model_name: Optional[str]) -> str:
    available = get_models()
    if model_name and model_name in available:
        return model_name
    return available[0]


def _build_story_payload(data: StoryRequest) -> dict:
    payload = {"trama": data.trama}
    if data.genero:
        payload["genero"] = data.genero
    if data.arco:
        payload["arco"] = data.arco
    if data.personajes:
        payload["personajes"] = data.personajes
    if data.experiment_id:
        payload["experiment_id"] = data.experiment_id
    return payload


def _build_schema_description(data: StoryRequest) -> str:
    parts = [f"Trama: {data.trama}"]
    if data.genero:
        parts.append(f"Género: {data.genero}")
    if data.arco:
        parts.append(f"Arco narrativo: {data.arco}")
    if data.experiment_id:
        parts.append(f"Experimento: {data.experiment_id}")
    return " | ".join(parts)


def _parse_aoi_response(response: str, available_names: List[str]) -> List[str]:
    response = (response or "").strip()
    if not response:
        return []

    available_map = {name.lower(): name for name in available_names}
    candidates: List[str] = []

    try:
        parsed = json.loads(response)
        if isinstance(parsed, dict):
            for key in ("aoi_names", "aois", "axis_of_interest"):
                value = parsed.get(key)
                if isinstance(value, list):
                    parsed = value
                    break
        if isinstance(parsed, list):
            candidates = [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass

    if not candidates:
        cleaned = response.replace("[", " ").replace("]", " ").replace("'", " ").replace('"', " ")
        for line in cleaned.splitlines():
            for token in line.split(","):
                token = token.strip()
                if token.startswith(("-", "*")):
                    token = token[1:].strip()
                if token:
                    candidates.append(token)

    normalized = _normalize_candidates(candidates, available_map)
    if normalized:
        return normalized

    lowered = response.lower()
    positions = []
    for name in available_names:
        idx = lowered.find(name.lower())
        if idx != -1:
            positions.append((idx, name))
    if positions:
        positions.sort()
        ordered = [name for _, name in positions]
        return _dedupe_keep_order(ordered)

    return []


def _normalize_candidates(candidates: List[str], available_map: dict[str, str]) -> List[str]:
    names: List[str] = []
    for candidate in candidates:
        cleaned = candidate.strip()
        if ":" in cleaned:
            cleaned = cleaned.split(":")[-1].strip()
        cleaned = cleaned.strip("-").strip("*").strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in available_map:
            name = available_map[key]
            if name not in names:
                names.append(name)
    return names


def _dedupe_keep_order(names: List[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        output.append(name)
    return output
