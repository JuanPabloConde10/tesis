"""
Phase 1: Selección y limpieza de los 5 cuentos seleccionados.

Lee los archivos originales de books/short-tales/, limpia artefactos de
navegación y metadata de Wikisource, y exporta data/selected_stories.json
con el texto limpio de cada cuento listo para el pipeline.
"""

import json
import os
import re
import sys

# Ensure project root is on the path when running this script directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BOOKS_DIR = os.path.join(os.path.dirname(__file__), "..", "books", "short-tales")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "selected_stories.json")

# The 5 selected stories with their first substantive line of body text.
# story_start_hint is used to locate the exact start of the narrative and
# skip the Wikisource header block (navigation + repeated title/author lines).
SELECTED_STORIES = [
    {
        "id": "prestamista",
        "title": "La leyenda del prestamista",
        "author": "Carlos Gagini",
        "filename": "La_leyenda_del_prestamista.txt",
        "story_start_hint": "En la mísera covacha",
    },
    {
        "id": "pericote",
        "title": "Breve historia veraz de un pericote",
        "author": "Abraham Valdelomar",
        "filename": "Breve_historia_veraz_de_un_pericote.txt",
        "story_start_hint": "Que concreta en la siguiente carta",
    },
    {
        "id": "diablo",
        "title": "El diablo y sus añicos",
        "author": "Hans Christian Andersen",
        "filename": "El_diablo_y_sus_añicos.txt",
        "story_start_hint": "Cierto día un duende malo",
    },
    {
        "id": "juguetes",
        "title": "Los juguetes",
        "author": "Juan José Morosoli",
        "filename": "Los_juguetes.txt",
        "story_start_hint": "Cuando mi madre estuvo grave",
    },
    {
        "id": "visita",
        "title": "Una visita infernal",
        "author": "Juana Manuela Gorriti",
        "filename": "Una_visita_infernal.txt",
        "story_start_hint": "Mi hermana a la edad",
    },
]

# Lines matching these patterns are always removed regardless of position
_SKIP_PATTERNS = [
    re.compile(r"^←"),
    re.compile(r"^→"),
    re.compile(r"^metadatos", re.IGNORECASE),
    re.compile(r"^Descargar como", re.IGNORECASE),
    re.compile(r"^Regresar a", re.IGNORECASE),
    re.compile(r"^\s*\.\s*$"),
    re.compile(r"^Portal", re.IGNORECASE),
    re.compile(r"^Categor", re.IGNORECASE),
]


def _is_noise_line(line: str) -> bool:
    stripped = line.strip()
    for pat in _SKIP_PATTERNS:
        if pat.match(stripped):
            return True
    return False


def clean_story(raw_text: str, story_start_hint: str) -> str:
    """
    Extract the narrative body from a raw Wikisource file.

    Strategy:
    1. Find the line index where the actual story body begins using
       story_start_hint (partial match against the first narrative sentence).
    2. Slice from that index onward.
    3. Remove trailing noise (e.g., "Regresar a …" footer).
    4. Collapse excessive blank lines.

    Falls back to removing noise lines from the full text when the hint
    is not found (e.g., files without a Wikisource header).
    """
    lines = raw_text.splitlines()
    start_idx = None

    for i, line in enumerate(lines):
        if story_start_hint.lower() in line.lower():
            start_idx = i
            break

    if start_idx is not None:
        body_lines = lines[start_idx:]
    else:
        # Fallback: remove noise lines from the whole file
        body_lines = [l for l in lines if not _is_noise_line(l)]

    # Remove trailing footer lines (e.g., "Regresar a Azul", "DIRECTORES: …")
    clean_lines = []
    for line in body_lines:
        if _is_noise_line(line):
            continue
        clean_lines.append(line)

    text = "\n".join(clean_lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def load_story(meta: dict) -> dict:
    path = os.path.join(BOOKS_DIR, meta["filename"])
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    text = clean_story(raw, meta["story_start_hint"])
    word_count = len(text.split())

    return {
        "id": meta["id"],
        "title": meta["title"],
        "author": meta["author"],
        "filename": meta["filename"],
        "text": text,
        "word_count": word_count,
    }


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    stories: dict = {}
    for meta in SELECTED_STORIES:
        print(f"Loading '{meta['title']}' by {meta['author']} ...")
        story = load_story(meta)
        stories[story["id"]] = story
        print(f"  {story['word_count']} words after cleaning\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(stories)} stories to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
