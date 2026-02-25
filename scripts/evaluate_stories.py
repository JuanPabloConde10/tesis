"""
Phase 4: Evaluación comparativa de cuentos originales vs. generados por LLM.

Para cada par (original, generado) en data/:
  1. Llama a un "judge LLM" que conoce cuál es el original pero no cómo
     fue generado el otro.
  2. El judge devuelve métricas estructuradas en JSON (escala 1-10).
  3. Guarda los resultados por cuento en data/evaluations/{story_id}.json
     y un resumen consolidado en data/evaluations/summary.json.

Uso:
    python scripts/evaluate_stories.py [--provider openai|gemini|local] [--model MODEL]
    python scripts/evaluate_stories.py --story-id prestamista   # solo un cuento
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

from infrastructure.llm_client.factory import resolve_client

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SELECTED_STORIES_FILE = os.path.join(DATA_DIR, "selected_stories.json")
GENERATED_DIR = os.path.join(DATA_DIR, "generated")
EVALUATIONS_DIR = os.path.join(DATA_DIR, "evaluations")

# ──────────────────────────────────────────────────────────────────────────────
# Judge prompt
# ──────────────────────────────────────────────────────────────────────────────

JUDGE_PROMPT = """\
Eres un crítico literario experto. Se te presentan dos versiones de un cuento:
el CUENTO ORIGINAL (escrito por un autor humano) y el CUENTO GENERADO (creado
por un sistema de inteligencia artificial que recibió las características
narrativas del original como input).

Tu tarea es evaluar ambos cuentos con las siguientes métricas (escala 1-10)
y devolver un objeto JSON con tus evaluaciones.

CUENTO ORIGINAL:
Título: {original_title}
Autor: {original_author}

\"\"\"
{original_text}
\"\"\"

CUENTO GENERADO:
\"\"\"
{generated_text}
\"\"\"

Evalúa con las siguientes métricas. Para cada una, asigna:
  - "original": puntuación 1-10 del cuento original
  - "generado": puntuación 1-10 del cuento generado

Métricas:
1. coherencia_narrativa: ¿Tiene inicio, nudo y desenlace coherentes y bien articulados?
2. desarrollo_personajes: ¿Los personajes tienen profundidad, motivaciones y personalidad?
3. consistencia_tematica: ¿El tema central se mantiene y se desarrolla a lo largo del texto?
4. calidad_estilo: ¿El lenguaje es fluido, expresivo y apropiado para el género?
5. preservacion_esencia: (solo para generado) ¿En qué medida el cuento generado captura el
   "espíritu" y los elementos esenciales del original? Puntúa también el original con 10.
6. calidad_global: Puntuación general del cuento (1-10).

Además incluye:
- "fortalezas_original": lista de 2-3 puntos fuertes del cuento original.
- "fortalezas_generado": lista de 2-3 puntos fuertes del cuento generado.
- "diferencias_clave": lista de 2-3 diferencias narrativas o estilísticas importantes
  entre ambos cuentos.
- "observaciones": párrafo libre (máximo 100 palabras) con tu análisis comparativo.

IMPORTANTE: Devuelve ÚNICAMENTE el objeto JSON, sin texto adicional, sin bloques
de código markdown, sin explicaciones fuera del JSON.

Formato esperado:
{{
  "coherencia_narrativa": {{"original": X, "generado": X}},
  "desarrollo_personajes": {{"original": X, "generado": X}},
  "consistencia_tematica": {{"original": X, "generado": X}},
  "calidad_estilo": {{"original": X, "generado": X}},
  "preservacion_esencia": {{"original": 10, "generado": X}},
  "calidad_global": {{"original": X, "generado": X}},
  "fortalezas_original": ["...", "...", "..."],
  "fortalezas_generado": ["...", "...", "..."],
  "diferencias_clave": ["...", "...", "..."],
  "observaciones": "..."
}}
"""

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _extract_json(text: str):
    """Extract a JSON object from an LLM response that may include extra text."""
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    idx = text.find("{")
    if idx != -1:
        depth = 0
        for i, ch in enumerate(text[idx:], start=idx):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[idx : i + 1])
                    except json.JSONDecodeError:
                        break

    raise ValueError(f"Could not extract valid JSON from LLM response:\n{text[:500]}")


def _compute_averages(evaluation: dict) -> dict:
    """Compute average scores across all numeric metrics for each version."""
    numeric_metrics = [
        "coherencia_narrativa",
        "desarrollo_personajes",
        "consistencia_tematica",
        "calidad_estilo",
        "preservacion_esencia",
        "calidad_global",
    ]
    original_scores = []
    generated_scores = []
    for metric in numeric_metrics:
        if metric in evaluation:
            entry = evaluation[metric]
            if isinstance(entry, dict):
                if "original" in entry:
                    original_scores.append(float(entry["original"]))
                if "generado" in entry:
                    generated_scores.append(float(entry["generado"]))

    avg_original = round(sum(original_scores) / len(original_scores), 2) if original_scores else None
    avg_generated = round(sum(generated_scores) / len(generated_scores), 2) if generated_scores else None
    return {"promedio_original": avg_original, "promedio_generado": avg_generated}


def evaluate_pair(
    story_id: str,
    original: dict,
    generated_text: str,
    client,
) -> dict:
    """Run the judge LLM for a single original/generated pair."""
    prompt = JUDGE_PROMPT.format(
        original_title=original["title"],
        original_author=original["author"],
        original_text=original["text"],
        generated_text=generated_text,
    )

    response = client.generate(
        prompt,
        system_prompt=None,
        temperature=0.2,
    )

    evaluation = _extract_json(response)
    averages = _compute_averages(evaluation)

    result = {
        "story_id": story_id,
        "title": original["title"],
        "author": original["author"],
        "word_count_original": original["word_count"],
        "word_count_generated": len(generated_text.split()),
        "metrics": evaluation,
        "averages": averages,
    }
    return result


def process_story(story_id: str, stories: dict, client) -> dict | None:
    if story_id not in stories:
        print(f"  SKIP: '{story_id}' not found in selected_stories.json")
        return None

    generated_path = os.path.join(GENERATED_DIR, f"{story_id}.txt")
    if not os.path.exists(generated_path):
        print(f"  SKIP: generated story not found at {generated_path}")
        return None

    with open(generated_path, "r", encoding="utf-8") as f:
        generated_text = f.read()

    original = stories[story_id]
    print(f"  Evaluating '{original['title']}' by {original['author']}...")
    result = evaluate_pair(story_id, original, generated_text, client)

    avg = result["averages"]
    print(f"  Avg scores -> original: {avg['promedio_original']} | generated: {avg['promedio_generado']}")
    return result


def build_summary(all_results: list[dict]) -> dict:
    """Build a consolidated summary across all evaluated stories."""
    summary_rows = []
    overall_original = []
    overall_generated = []

    for r in all_results:
        avg = r["averages"]
        summary_rows.append(
            {
                "story_id": r["story_id"],
                "title": r["title"],
                "author": r["author"],
                "promedio_original": avg["promedio_original"],
                "promedio_generado": avg["promedio_generado"],
                "diferencia": (
                    round(avg["promedio_generado"] - avg["promedio_original"], 2)
                    if avg["promedio_original"] is not None and avg["promedio_generado"] is not None
                    else None
                ),
            }
        )
        if avg["promedio_original"] is not None:
            overall_original.append(avg["promedio_original"])
        if avg["promedio_generado"] is not None:
            overall_generated.append(avg["promedio_generado"])

    global_avg_original = (
        round(sum(overall_original) / len(overall_original), 2) if overall_original else None
    )
    global_avg_generated = (
        round(sum(overall_generated) / len(overall_generated), 2) if overall_generated else None
    )

    return {
        "total_stories_evaluated": len(all_results),
        "global_avg_original": global_avg_original,
        "global_avg_generated": global_avg_generated,
        "global_diferencia": (
            round(global_avg_generated - global_avg_original, 2)
            if global_avg_original is not None and global_avg_generated is not None
            else None
        ),
        "per_story": summary_rows,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate original vs. generated stories using a judge LLM."
    )
    parser.add_argument(
        "--provider",
        default=os.getenv("DEFAULT_PROVIDER", "openai"),
        choices=["openai", "gemini", "local"],
        help="LLM provider to use",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (default: gpt-4o-mini for openai, gemini-2.0-flash for gemini)",
    )
    parser.add_argument(
        "--story-id",
        default=None,
        help="Evaluate only a specific story ID. Defaults to all.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    model_defaults = {
        "openai": "gpt-4o-mini",
        "gemini": "gemini-2.5-flash",
        "local": "local-model",
    }
    model = args.model or model_defaults.get(args.provider, "gpt-4o-mini")

    print(f"Provider: {args.provider} | Model: {model}")
    client = resolve_client(args.provider, model)

    with open(SELECTED_STORIES_FILE, "r", encoding="utf-8") as f:
        stories = json.load(f)

    os.makedirs(EVALUATIONS_DIR, exist_ok=True)

    if args.story_id:
        story_ids = [args.story_id]
    else:
        # Evaluate all stories that have a generated version
        story_ids = [
            f.replace(".txt", "")
            for f in os.listdir(GENERATED_DIR)
            if f.endswith(".txt") and not f.endswith("_meta.json")
        ]
        story_ids.sort()

    if not story_ids:
        print("No generated stories found. Run generate_stories.py first.")
        sys.exit(1)

    print(f"Evaluating stories: {story_ids}\n")

    all_results = []
    for story_id in story_ids:
        print(f"\n--- {story_id} ---")
        result = process_story(story_id, stories, client)
        if result is None:
            continue

        out_path = os.path.join(EVALUATIONS_DIR, f"{story_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  Saved to {out_path}")

        all_results.append(result)

    if all_results:
        summary = build_summary(all_results)
        summary_path = os.path.join(EVALUATIONS_DIR, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*50}")
        print(f"SUMMARY ({summary['total_stories_evaluated']} stories)")
        print(f"  Global avg original:  {summary['global_avg_original']}")
        print(f"  Global avg generated: {summary['global_avg_generated']}")
        print(f"  Difference:           {summary['global_diferencia']}")
        print(f"  Saved to {summary_path}")


if __name__ == "__main__":
    main()
