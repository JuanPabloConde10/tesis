"""
Phase 3: Generación de cuentos a partir de las features extraídas.

Para cada story en data/features/{story_id}.json:
  1. Construye un StoryRequest con los AOIs, trama y personajes extraídos.
  2. Llama a generate_story_mode2() del pipeline neuro-simbólico existente.
  3. Puede generar N candidatos, evaluarlos con LLM juez y seleccionar ganador(es).
  4. Guarda resultados en data/generated-story-LaaJ/{story_id}/{story_id}_*.

Uso:
    python scripts/generate_stories.py [--provider openai|gemini|local] [--model MODEL]
    python scripts/generate_stories.py --story-id prestamista   # solo un cuento
"""

import argparse
import json
import os
import sys
import time
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

from google.genai.errors import ClientError
from infrastructure.llm_client.factory import resolve_client
from infrastructure.api.global_schemas import StoryRequest
from story_creator.mode2 import generate_story_mode2
from evaluation import evaluate_generated_story_dimensions, rank_candidates

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FEATURES_DIR = os.path.join(DATA_DIR, "features")
GENERATED_DIR = os.path.join(DATA_DIR, "generated-story-LaaJ")


def _extract_character_names(characters: list[str]) -> list[str]:
    """
    Convert feature characters like ["protagonista: usurero anciano"] to a
    list of role labels that can be used as character placeholders.
    The story generator will assign real names to these placeholders.
    """
    names = []
    for char in characters:
        # Take the part after the colon if present, e.g. "protagonista: usurero" -> "usurero"
        if ":" in char:
            role_label = char.split(":", 1)[1].strip()
        else:
            role_label = char.strip()
        if role_label:
            names.append(role_label)
    return names or ["Protagonista"]


def generate_story_from_features(features: dict, client) -> str:
    """
    Build a StoryRequest from extracted features and call generate_story_mode2.
    """
    character_names = _extract_character_names(features.get("characters", []))

    # Build a rich trama description that includes genre, tone and plot_summary
    trama_parts = []
    if features.get("plot_summary"):
        trama_parts.append(features["plot_summary"])
    if features.get("tone"):
        trama_parts.append(f"Tono: {features['tone']}.")
    if features.get("themes"):
        trama_parts.append(f"Temas: {', '.join(features['themes'])}.")

    trama = " ".join(trama_parts) or features.get("title", "")

    request = StoryRequest(
        trama=trama,
        genero=features.get("genre", ""),
        personajes=character_names,
        aoi_names=features.get("aoi_names", ["CONFLICT"]),
        strategy="sequential",
        generation_method="aoi_directo",
        temperature=0.7,
    )

    story_text = generate_story_mode2(request, client, temperature=0.7)
    return story_text


def generate_story_candidate_from_features(
    features: dict,
    client,
    *,
    candidate_idx: int,
) -> str:
    character_names = _extract_character_names(features.get("characters", []))

    trama_parts = []
    if features.get("plot_summary"):
        trama_parts.append(features["plot_summary"])
    if features.get("tone"):
        trama_parts.append(f"Tono: {features['tone']}.")
    if features.get("themes"):
        trama_parts.append(f"Temas: {', '.join(features['themes'])}.")
    trama = " ".join(trama_parts) or features.get("title", "")

    request = StoryRequest(
        trama=trama,
        genero=features.get("genre", ""),
        personajes=character_names,
        aoi_names=features.get("aoi_names", ["CONFLICT"]),
        strategy="sequential",
        generation_method="aoi_directo",
        temperature=0.7,
    )
    return generate_story_mode2(
        request,
        client,
        temperature=0.7,
        seed=42 + candidate_idx,
    )


def _parse_weighted_weights(raw: Optional[str]) -> Optional[dict]:
    if raw is None:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as err:
        raise ValueError("--weighted-weights debe ser un JSON válido") from err
    if not isinstance(parsed, dict):
        raise ValueError("--weighted-weights debe ser un objeto JSON")
    return parsed


def _default_policies(num_candidates: int, policies: Optional[list[str]]) -> list[str]:
    if policies:
        return policies
    if num_candidates > 1:
        return ["mean"]
    return []


def _attach_policy_scores(
    candidates: list[dict],
    rankings: dict,
) -> list[dict]:
    scores_index: dict[int, dict[str, Optional[float]]] = {}
    for policy, rows in rankings.items():
        for row in rows:
            candidate_id = int(row["candidate_id"])
            if candidate_id not in scores_index:
                scores_index[candidate_id] = {}
            scores_index[candidate_id][policy] = row.get("score")

    out = []
    for candidate in candidates:
        entry = dict(candidate)
        entry["policy_scores"] = scores_index.get(int(candidate["candidate_id"]), {})
        out.append(entry)
    return out


def process_story(
    story_id: str,
    client,
    *,
    num_candidates: int = 1,
    selection_policies: Optional[list[str]] = None,
    weighted_policy_weights: Optional[dict] = None,
) -> None:
    features_path = os.path.join(FEATURES_DIR, f"{story_id}.json")
    if not os.path.exists(features_path):
        print(f"  SKIP: features file not found at {features_path}")
        return

    with open(features_path, "r", encoding="utf-8") as f:
        features = json.load(f)

    print(f"  Title: {features['title']}")
    print(f"  Author: {features['author']}")
    print(f"  AOIs: {features['aoi_names']}")
    print(f"  Generating {num_candidates} candidate(s)...")
    policies = _default_policies(num_candidates, selection_policies)
    if "weighted" in policies and weighted_policy_weights is None:
        raise ValueError(
            "Policy 'weighted' requiere --weighted-weights con novelty/sensicality/pragmaticality"
        )

    candidates = []
    for candidate_idx in range(num_candidates):
        print(f"    Candidate {candidate_idx + 1}/{num_candidates}...")
        for attempt in range(3):
            try:
                generated_text = generate_story_candidate_from_features(
                    features, client, candidate_idx=candidate_idx
                )
                break
            except ClientError as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait = 45 if attempt < 2 else 0
                    if wait:
                        print(f"    Rate limit (429), waiting {wait}s before retry...")
                        time.sleep(wait)
                    else:
                        raise
                else:
                    raise
        candidates.append(
            {
                "candidate_id": candidate_idx + 1,
                "story": generated_text,
                "word_count": len(generated_text.split()),
            }
        )

    if policies:
        print(f"  Evaluating candidates with policies: {policies}")
        evaluated_candidates = []
        for candidate in candidates:
            evaluation = evaluate_generated_story_dimensions(
                candidate["story"],
                client,
                metadata={"story_id": story_id, "candidate_id": candidate["candidate_id"]},
            )
            evaluated_candidates.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "story": candidate["story"],
                    "word_count": candidate["word_count"],
                    "evaluation": evaluation,
                }
            )

        ranking = rank_candidates(
            evaluated_candidates,
            policies=policies,
            weighted_policy_weights=weighted_policy_weights,
        )
        winners = ranking["winners"]
        primary_policy = ranking["policies"][0]
        primary_winner = winners[primary_policy]
        selected_story = primary_winner["story"]
        selected_word_count = primary_winner["word_count"]

        candidates_for_json = _attach_policy_scores(
            evaluated_candidates,
            ranking["rankings"],
        )
        selected_stories_by_policy = {
            policy: winner["story"] for policy, winner in winners.items()
        }
    else:
        ranking = None
        winners = {}
        primary_policy = None
        selected_story = candidates[0]["story"]
        selected_word_count = candidates[0]["word_count"]
        candidates_for_json = candidates
        selected_stories_by_policy = {}

    story_output_dir = os.path.join(GENERATED_DIR, story_id)
    os.makedirs(story_output_dir, exist_ok=True)

    out_path = os.path.join(story_output_dir, f"{story_id}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(selected_story)

    winner_txt_path = os.path.join(story_output_dir, f"{story_id}_winner.txt")
    with open(winner_txt_path, "w", encoding="utf-8") as f:
        f.write(selected_story)

    mean_story = selected_stories_by_policy.get("mean")
    if mean_story:
        mean_txt_path = os.path.join(story_output_dir, f"{story_id}_mean.txt")
        with open(mean_txt_path, "w", encoding="utf-8") as f:
            f.write(mean_story)

    weighted_story = selected_stories_by_policy.get("weighted")
    if weighted_story:
        weighted_txt_path = os.path.join(story_output_dir, f"{story_id}_weighted.txt")
        with open(weighted_txt_path, "w", encoding="utf-8") as f:
            f.write(weighted_story)

    meta_payload = {
        "story_id": story_id,
        "source_title": features["title"],
        "source_author": features["author"],
        "aoi_names_used": features["aoi_names"],
        "generation_method": "aoi_directo",
        "strategy": "sequential",
        "word_count": selected_word_count,
        "num_candidates": num_candidates,
        "selection_policies": policies,
        "primary_policy": primary_policy,
    }
    if ranking:
        meta_payload["weighted_policy_weights_normalized"] = ranking.get(
            "weighted_policy_weights_normalized"
        )
        meta_payload["winner_candidate_ids"] = {
            policy: winner["candidate_id"] for policy, winner in winners.items()
        }

    meta_path = os.path.join(story_output_dir, f"{story_id}_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, ensure_ascii=False, indent=2)

    candidates_path = os.path.join(story_output_dir, f"{story_id}_candidates.json")
    with open(candidates_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "story_id": story_id,
                "num_candidates": num_candidates,
                "selection_policies": policies,
                "candidates": candidates_for_json,
                "rankings": ranking["rankings"] if ranking else {},
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    winners_path = os.path.join(story_output_dir, f"{story_id}_winners.json")
    with open(winners_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "story_id": story_id,
                "primary_policy": primary_policy,
                "winners": winners,
                "selected_stories_by_policy": selected_stories_by_policy,
                "winner_story": selected_story,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"  Selected story ({selected_word_count} words) -> {out_path}")
    if ranking:
        print(
            "  Winners by policy: "
            + ", ".join(
                f"{policy}=candidate_{winner['candidate_id']}"
                for policy, winner in winners.items()
            )
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate stories from extracted features using the neuro-symbolic pipeline."
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
        help="Process only a specific story ID (e.g. prestamista). Defaults to all.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=15.0,
        help="Seconds to wait between stories to respect rate limits (default: 15)",
    )
    parser.add_argument(
        "--num-candidates",
        type=int,
        default=1,
        help="Cantidad de candidatos por cuento antes de seleccionar (default: 1)",
    )
    parser.add_argument(
        "--selection-policies",
        nargs="+",
        choices=["mean", "weighted"],
        default=None,
        help="Políticas de selección a aplicar (mean weighted)",
    )
    parser.add_argument(
        "--weighted-weights",
        default=None,
        help='Pesos para policy weighted como JSON, ej: {"novelty":0.5,"sensicality":0.25,"pragmaticality":0.25}',
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
    weighted_weights = _parse_weighted_weights(args.weighted_weights)

    if args.num_candidates < 1:
        raise ValueError("--num-candidates debe ser >= 1")
    policies = _default_policies(args.num_candidates, args.selection_policies)
    if "weighted" in policies and weighted_weights is None:
        raise ValueError(
            "Si usás policy 'weighted', debés pasar --weighted-weights con novelty/sensicality/pragmaticality"
        )

    os.makedirs(GENERATED_DIR, exist_ok=True)

    if args.story_id:
        story_ids = [args.story_id]
    else:
        # Discover all feature files
        story_ids = [
            f.replace(".json", "")
            for f in os.listdir(FEATURES_DIR)
            if f.endswith(".json") and not f.endswith("_meta.json")
        ]
        story_ids.sort()

    if not story_ids:
        print("No feature files found. Run extract_features.py first.")
        sys.exit(1)

    print(f"Generating stories for: {story_ids}\n")

    for i, story_id in enumerate(story_ids):
        if i > 0:
            print(f"  Waiting {args.delay}s before next story...")
            time.sleep(args.delay)
        print(f"\n--- {story_id} ---")
        process_story(
            story_id,
            client,
            num_candidates=args.num_candidates,
            selection_policies=policies,
            weighted_policy_weights=weighted_weights,
        )

    print(f"\nDone. Generated stories saved to {GENERATED_DIR}/<story_id>/")


if __name__ == "__main__":
    main()
