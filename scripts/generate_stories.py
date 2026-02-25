"""
Phase 3: Generación de cuentos a partir de las features extraídas.

Para cada story en data/features/{story_id}.json:
  1. Construye un StoryRequest con los AOIs, trama y personajes extraídos.
  2. Llama a generate_story_mode2() del pipeline neuro-simbólico existente.
  3. Guarda el cuento generado en data/generated/{story_id}.txt.

Uso:
    python scripts/generate_stories.py [--provider openai|gemini|local] [--model MODEL]
    python scripts/generate_stories.py --story-id prestamista   # solo un cuento
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

from google.genai.errors import ClientError
from infrastructure.llm_client.factory import resolve_client
from infrastructure.api.global_schemas import StoryRequest
from story_creator.mode2 import generate_story_mode2

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FEATURES_DIR = os.path.join(DATA_DIR, "features")
GENERATED_DIR = os.path.join(DATA_DIR, "generated")


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


def process_story(story_id: str, client) -> None:
    features_path = os.path.join(FEATURES_DIR, f"{story_id}.json")
    if not os.path.exists(features_path):
        print(f"  SKIP: features file not found at {features_path}")
        return

    with open(features_path, "r", encoding="utf-8") as f:
        features = json.load(f)

    print(f"  Title: {features['title']}")
    print(f"  Author: {features['author']}")
    print(f"  AOIs: {features['aoi_names']}")
    print(f"  Generating story...")

    for attempt in range(3):
        try:
            generated_text = generate_story_from_features(features, client)
            break
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait = 45 if attempt < 2 else 0
                if wait:
                    print(f"  Rate limit (429), waiting {wait}s before retry...")
                    time.sleep(wait)
                else:
                    raise
            else:
                raise
    word_count = len(generated_text.split())

    out_path = os.path.join(GENERATED_DIR, f"{story_id}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(generated_text)

    # Also save a metadata JSON alongside
    meta_path = os.path.join(GENERATED_DIR, f"{story_id}_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "story_id": story_id,
                "source_title": features["title"],
                "source_author": features["author"],
                "aoi_names_used": features["aoi_names"],
                "generation_method": "aoi_directo",
                "strategy": "sequential",
                "word_count": word_count,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"  Generated {word_count} words -> {out_path}")


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
        process_story(story_id, client)

    print(f"\nDone. Generated stories saved to {GENERATED_DIR}/")


if __name__ == "__main__":
    main()
