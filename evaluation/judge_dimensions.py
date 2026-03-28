import json
import re
from typing import Any, Optional

DIMENSIONS = ("novelty", "sensicality", "pragmaticality")

JUDGE_DIMENSIONS_PROMPT = """\
Eres un crítico literario experto en evaluación de creatividad textual.

Evalúa el siguiente cuento en una escala de 1 a 10 en las dimensiones:
- novelty
- sensicality
- pragmaticality

Debes responder SOLO con un JSON válido, sin texto adicional ni markdown.

Formato:
{{
  "novelty": X,
  "sensicality": X,
  "pragmaticality": X,
  "justification": "explicación breve en 2-4 oraciones"
}}

Cuento a evaluar:
\"\"\"
{story_text}
\"\"\"
"""


def _extract_json(text: str) -> dict[str, Any]:
    """Extract a JSON object from an LLM response that may include extra text."""
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
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
                    parsed = json.loads(text[idx : i + 1])
                    if isinstance(parsed, dict):
                        return parsed
                    break

    raise ValueError(f"Could not extract valid JSON from LLM response:\n{text[:500]}")


def _to_score(value: Any) -> Optional[float]:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    return round(min(10.0, max(1.0, score)), 2)


def _normalize_dimensions(eval_raw: dict[str, Any]) -> dict[str, Optional[float]]:
    out: dict[str, Optional[float]] = {}
    for dim in DIMENSIONS:
        out[dim] = _to_score(eval_raw.get(dim))
    return out


def _average_dimensions(dimensions: dict[str, Optional[float]]) -> Optional[float]:
    values = [x for x in dimensions.values() if x is not None]
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def evaluate_generated_story_dimensions(
    story_text: str,
    client: Any,
    metadata: Optional[dict[str, Any]] = None,
    *,
    temperature: float = 0.2,
    include_raw_response: bool = False,
) -> dict[str, Any]:
    """Evaluate a single generated story in the 3 paper dimensions."""
    prompt = JUDGE_DIMENSIONS_PROMPT.format(story_text=story_text)
    raw_response = client.generate(prompt, system_prompt=None, temperature=temperature)
    parsed = _extract_json(raw_response)
    dimensions = _normalize_dimensions(parsed)

    result: dict[str, Any] = {
        "dimensions": dimensions,
        "average_score": _average_dimensions(dimensions),
        "justification": str(parsed.get("justification", "") or "").strip(),
    }

    if metadata:
        result["metadata"] = metadata
    if include_raw_response:
        result["raw_response"] = raw_response
    return result
