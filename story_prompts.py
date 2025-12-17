import ast
import json
import os
from typing import List, Optional

from openai import OpenAI

from axis_of_interest.prompts import prompt_contexto_axis_of_interest, template_prompt_generate_plot_schema
from axis_of_interest.schemas import list_of_aoi
from story_models import ARC_LABELS, StoryRequest


def _openai_chat(
    prompt: str,
    *,
    model: str,
    system: Optional[str],
    temperature: Optional[float],
    max_tokens: Optional[int],
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def _extract_json_block(text: str, prefer_list: bool = False) -> Optional[str]:
    """Extrae el primer bloque JSON (lista u objeto) de un string medio ruidoso."""
    if prefer_list:
        start, end = text.find("["), text.rfind("]")
    else:
        start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return None


def _parse_dict_like(raw: str) -> Optional[dict]:
    """Intenta convertir una respuesta ruidosa en dict."""
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    block = _extract_json_block(raw, prefer_list=False)
    if block:
        try:
            parsed = json.loads(block)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return None


def _sanitize_axis_list(axis_list: List[str]) -> List[str]:
    valid_names = {aoi.name for aoi in list_of_aoi}
    cleaned = [axis for axis in axis_list if axis in valid_names]
    if cleaned:
        return cleaned
    # si no se reconocen, usa dos ejes conocidos para mantener la coherencia
    return list(valid_names)[:2]


def build_story_prompt(data: StoryRequest, modo: str) -> str:
    if modo == "0":
        return modo0(data)
    if modo == "2":
        return modo2(data)
    raise RuntimeError(f"El modo {modo} no usa un prompt simple.")


def modo0(data: StoryRequest) -> str:
    personajes = ", ".join(data.personajes) if data.personajes else "No especificados"
    genero = data.genero or "Libre"
    arco = ARC_LABELS.get(data.arco, data.arco) if data.arco else "Libre"
    return (
        "Escribe un cuento breve en español usando los datos proporcionados.\n"
        f"- Descripción de la trama: {data.trama}\n"
        f"- Personajes principales: {personajes}\n"
        f"- Género: {genero}\n"
        f"- Arco narrativo: {arco}\n\n"
        "Extensión: 3 a 5 párrafos. Mantén un tono acorde al género y cierra con un desenlace claro. "
        "Responde solo con el cuento."
    )


def _extract_axis_of_interest(data: StoryRequest, model: str) -> List[str]:
    available = ", ".join(aoi.name for aoi in list_of_aoi)
    prompt = (
        f"{prompt_contexto_axis_of_interest}\n"
        f"Dada la siguiente sinopsis, devuelve solo un arreglo JSON con los nombres de los Axis of Interest relevantes.\n"
        f"Usa únicamente estos nombres: {available}.\n\n"
        f"Sinopsis: {data.trama}\n\n"
        'Responde solo el arreglo JSON, ejemplo: ["DONOR","CONFLICT"].'
    )
    raw = _openai_chat(
        prompt=prompt,
        model=model,
        system="Eres un analista narrativo experto en identificar ejes de interés.",
        temperature=0,
        max_tokens=200,
    )
    # Intento de parseo robusto
    candidates = [raw]
    block = _extract_json_block(raw, prefer_list=True)
    if block:
        candidates.insert(0, block)

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list):
                cleaned = [str(item) for item in parsed if isinstance(item, str)]
                if cleaned:
                    return cleaned
        except json.JSONDecodeError:
            continue

    fallback = [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]
    return fallback or ["CONFLICT", "DONOR"]  # fallback mínimo


def _generate_plot_schema(data: StoryRequest, axis_list: List[str], model: str) -> dict:
    personajes = ", ".join(data.personajes) if data.personajes else "No especificados"
    genero = data.genero or "Libre"
    arco = ARC_LABELS.get(data.arco, data.arco) if data.arco else "Libre"
    axis_clean = _sanitize_axis_list(axis_list)
    axis_str = ", ".join(axis_clean) if axis_clean else "N/A"

    prompt = (
        f"{prompt_contexto_axis_of_interest}\n"
        f"Sinopsis: {data.trama}\n"
        f"Personajes: {personajes}\n"
        f"Género: {genero}\n"
        f"Arco narrativo: {arco}\n\n"
        + template_prompt_generate_plot_schema.format(axis_of_interest=axis_str)
        + "\nDevuelve solo el JSON del Plot Schema."
    )
    raw = _openai_chat(
        prompt=prompt,
        model=model,
        system="Eres un planificador narrativo que genera plot schemas coherentes.",
        temperature=0.3,
        max_tokens=800,
    )
    parsed = _parse_dict_like(raw)
    if parsed is None:
        raise RuntimeError("No se pudo generar un Plot Schema válido en modo 1.")
    return parsed


def _fallback_plot_schema(axis_list: List[str]) -> dict:
    """Crea un plot schema sencillo combinando spans de los AOI conocidos."""
    axis_by_name = {aoi.name: aoi for aoi in list_of_aoi}
    spans = []
    for axis in axis_list:
        aoi = axis_by_name.get(axis)
        if aoi:
            spans.extend([span.model_dump() for span in aoi.plot_spans])

    if not spans and list_of_aoi:
        spans = [span.model_dump() for span in list_of_aoi[0].plot_spans]

    return {
        "id": "fallback-schema",
        "name": "Plot Schema generado",
        "description": "Schema generado automáticamente como fallback.",
        "plots_span": spans,
    }


def _generate_story_from_schema(
    data: StoryRequest,
    plot_schema: dict,
    model: str,
    temperature: Optional[float],
    max_tokens: Optional[int],
) -> str:
    personajes = ", ".join(data.personajes) if data.personajes else "No especificados"
    genero = data.genero or "Libre"
    arco = ARC_LABELS.get(data.arco, data.arco) if data.arco else "Libre"
    prompt = (
        f"{prompt_contexto_axis_of_interest}\n"
        "Escribe un cuento en español en 3 a 5 párrafos a partir del siguiente Plot Schema y datos base.\n"
        f"Datos base:\n"
        f"- Sinopsis: {data.trama}\n"
        f"- Personajes: {personajes}\n"
        f"- Género: {genero}\n"
        f"- Arco narrativo: {arco}\n\n"
        f"Plot Schema: {json.dumps(plot_schema, ensure_ascii=False)}\n\n"
        "Responde solo con el cuento final, mantén coherencia con el esquema."
    )
    return _openai_chat(
        prompt=prompt,
        model=model,
        system="Eres un escritor creativo de cuentos cortos.",
        temperature=temperature,
        max_tokens=max_tokens,
    )


def run_mode1_story(
    data: StoryRequest, *, model: str, temperature: Optional[float], max_tokens: Optional[int]
) -> str:
    axis_list = _extract_axis_of_interest(data, model=model)
    print(axis_list)
    plot_schema = _fallback_plot_schema(axis_list=axis_list)
    #plot_schema = _generate_plot_schema(data, axis_list=axis_list, model=model)
    print(plot_schema)
    return _generate_story_from_schema(
        data=data,
        plot_schema=plot_schema,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def modo2(data: StoryRequest) -> str:
    return "Modo 2 aún no está implementado."
