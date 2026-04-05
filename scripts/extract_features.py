"""
Phase 2: Extracción de features narrativas de los cuentos seleccionados.

Para cada cuento en data/selected_stories.json:
  1. Llama al LLM con un prompt de extracción de features generales
     (género, personajes, escenario, temas, tono, estilo narrativo, resumen).
  2. Llama al LLM con el prompt existente para identificar los AOIs presentes.
  3. Combina ambos resultados en un StoryFeatures JSON.
  4. Guarda en data/features/{story_id}.json.

Uso:
    python scripts/extract_features.py [--provider openai|gemini|local] [--model MODEL]
"""

import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

from infrastructure.llm_client.factory import resolve_client
from axis_of_interest.registry import list_of_aoi

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SELECTED_STORIES_FILE = os.path.join(DATA_DIR, "selected_stories.json")
FEATURES_DIR = os.path.join(DATA_DIR, "features")

# All AOI names available in the system
ALL_AOI_NAMES = [aoi.name for aoi in list_of_aoi]

# ──────────────────────────────────────────────────────────────────────────────
# Prompts
# ──────────────────────────────────────────────────────────────────────────────

PROMPT_GENERAL_FEATURES = """\
Eres un experto en narratología y análisis literario. A continuación te presento
un cuento. Tu tarea es analizar sus características narrativas y devolver un
objeto JSON con los siguientes campos:

- "genre": string con el género principal del cuento. Valores posibles (no
  exclusivos): "cuento_moral", "cuento_de_hadas", "horror_gotico",
  "realismo_magico", "memoria_autobiografica", "thriller", "fabula",
  "cuento_fantástico", u otro género si corresponde.
- "setting": string describiendo el escenario espacio-temporal del cuento
  (máximo 2 oraciones).
- "characters": lista de strings describiendo los personajes con su rol
  narrativo. Ejemplo: ["protagonista: usurero anciano", "antagonista: la
  codicia personificada"].
- "themes": lista de strings con los temas centrales del cuento.
- "tone": string describiendo el tono emocional dominante (e.g., "oscuro y
  moralista", "filosófico y melancólico", "humorístico", "ominoso").
- "narrative_style": string describiendo la voz y estilo narrativo (e.g.,
  "narrador omnisciente en tercera persona", "narrador en primera persona",
  "epistolar").
- "plot_summary": string con un resumen del arco narrativo completo en 3-4
  oraciones. Debe cubrir inicio, conflicto central y desenlace.

IMPORTANTE: Devuelve ÚNICAMENTE el objeto JSON, sin texto adicional, sin
bloques de código markdown, sin explicaciones.

Cuento:
\"\"\"
{story_text}
\"\"\"
"""

PROMPT_AOI_DETECTION = """\
Eres un experto en narrativa. Trabajas en un proyecto de escritura de cuentos
siguiendo un método neuro-simbólico basado en "Axis of Interest" (AOIs).

Los AOIs disponibles en el sistema son los siguientes (nombre - descripción):
{aoi_list}

Dado el siguiente cuento, identifica qué AOIs están presentes o son relevantes
para representar su estructura narrativa. Selecciona entre 1 y 3 AOIs que mejor
capturen la trama.

IMPORTANTE: Devuelve ÚNICAMENTE una lista JSON de strings con los nombres
exactos de los AOIs seleccionados (tal como aparecen arriba), sin texto
adicional, sin bloques de código markdown.

Ejemplo de respuesta válida: ["CONFLICT", "RAGS 2 RICHES"]

Cuento:
\"\"\"
{story_text}
\"\"\"
"""


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_aoi_list_str() -> str:
    lines = []
    for aoi in list_of_aoi:
        lines.append(f"- {aoi.name}: {aoi.description}")
    return "\n".join(lines)


def _extract_json(text: str):
    """
    Extract a JSON object or array from an LLM response that may contain
    surrounding prose or markdown code fences.
    """
    # Try to find a JSON block in ```json ... ``` or ``` ... ```
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    # Try to parse as-is
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find the first { or [ and extract from there
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        idx = text.find(start_char)
        if idx != -1:
            # Find matching closing bracket
            depth = 0
            for i, ch in enumerate(text[idx:], start=idx):
                if ch == start_char:
                    depth += 1
                elif ch == end_char:
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[idx:i + 1])
                        except json.JSONDecodeError:
                            break

    raise ValueError(f"Could not extract valid JSON from LLM response:\n{text[:500]}")


def _call_llm(client, prompt: str, temperature: float, delay: float = 5.0):
    """Call the LLM and wait `delay` seconds afterward to respect rate limits."""
    response = client.generate(prompt, system_prompt=None, temperature=temperature)
    if delay > 0:
        time.sleep(delay)
    return response


def extract_features_for_story(story: dict, client, delay: float = 5.0) -> dict:
    """Run both prompts for a single story and merge the results."""
    story_text = story["text"]

    print(f"  [1/2] Extracting general features...")
    prompt_general = PROMPT_GENERAL_FEATURES.format(story_text=story_text)
    response_general = _call_llm(client, prompt_general, temperature=0.2, delay=delay)
    general = _extract_json(response_general)

    print(f"  [2/2] Detecting AOIs...")
    aoi_list_str = _build_aoi_list_str()
    prompt_aoi = PROMPT_AOI_DETECTION.format(
        aoi_list=aoi_list_str,
        story_text=story_text,
    )
    response_aoi = _call_llm(client, prompt_aoi, temperature=0.1, delay=delay)
    aoi_names = _extract_json(response_aoi)

    # Validate that the returned AOI names exist in the system
    valid_aoi_names = [n for n in aoi_names if n in ALL_AOI_NAMES]
    if not valid_aoi_names:
        # Fallback: use CONFLICT as the most generic AOI
        valid_aoi_names = ["CONFLICT"]
        print(f"  WARNING: No valid AOIs found in response, falling back to CONFLICT")

    features = {
        "story_id": story["id"],
        "title": story["title"],
        "author": story["author"],
        "genre": general.get("genre", ""),
        "setting": general.get("setting", ""),
        "characters": general.get("characters", []),
        "themes": general.get("themes", []),
        "tone": general.get("tone", ""),
        "narrative_style": general.get("narrative_style", ""),
        "plot_summary": general.get("plot_summary", ""),
        "aoi_names": valid_aoi_names,
    }
    return features


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract narrative features from selected stories using an LLM."
    )
    parser.add_argument(
        "--provider",
        default=os.getenv("DEFAULT_PROVIDER", "openai"),
        choices=["openai", "gemini", "local"],
        help="LLM provider to use (default: value of DEFAULT_PROVIDER env var or 'openai')",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (default: gpt-4o-mini for openai, gemini-2.5-flash for gemini)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="Seconds to wait between API calls to respect rate limits (default: 5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Default models per provider
    model_defaults = {
        "openai": "gpt-4o-mini",
        "gemini": "gemini-2.5-flash",
        "local": "local-model",
    }
    model = args.model or model_defaults.get(args.provider, "gpt-4o-mini")

    print(f"Provider: {args.provider} | Model: {model} | Delay between calls: {args.delay}s")
    client = resolve_client(args.provider, model)

    with open(SELECTED_STORIES_FILE, "r", encoding="utf-8") as f:
        stories = json.load(f)

    os.makedirs(FEATURES_DIR, exist_ok=True)

    for story_id, story in stories.items():
        print(f"\nProcessing: '{story['title']}' by {story['author']}")
        features = extract_features_for_story(story, client, delay=args.delay)

        out_path = os.path.join(FEATURES_DIR, f"{story_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(features, f, ensure_ascii=False, indent=2)

        print(f"  Saved features to {out_path}")
        print(f"  AOIs detected: {features['aoi_names']}")
        print(f"  Genre: {features['genre']} | Tone: {features['tone']}")

    print(f"\nDone. Features saved to {FEATURES_DIR}/")


if __name__ == "__main__":
    main()
