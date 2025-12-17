import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

from experiments.data import get_experiments
from story_models import StoryRequest
from story_prompts import build_story_prompt, run_mode1_story

load_dotenv()

BASE_PATH = Path(__file__).parent
WEB_DIR = BASE_PATH / "web"

api = FastAPI(title="Taller de cuentos")

AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
DEFAULT_MODEL = AVAILABLE_MODELS[0]

MODES = [
    {"id": "0", "name": "Modo 0", "description": "Generación a pelo."},
    {"id": "1", "name": "Modo 1", "description": "Utilizando el Plot Schema en el prompt"},
    {"id": "2", "name": "Modo 2", "description": "Creamos el Plot Schema y chunks para cada escena. Luego le pedimos al LLM que hile estas escenas en un unico cuento"},
]
DEFAULT_MODE = MODES[0]["id"]


def resolve_model(model_name: Optional[str]) -> str:
    if model_name:
        if model_name not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail=f"Modelo no habilitado: {model_name}")
        return model_name
    return DEFAULT_MODEL


def resolve_mode(mode_name: Optional[str]) -> dict:
    mode_id = mode_name or DEFAULT_MODE
    for mode in MODES:
        if mode["id"] == mode_id:
            return mode
    raise HTTPException(status_code=400, detail=f"Modo de creación desconocido: {mode_id}")


def generate_with_openai(
    prompt: str, temperature: Optional[float], max_tokens: Optional[int], model: str
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un escritor creativo de cuentos cortos."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


@api.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html no encontrado")
    return FileResponse(index_path)


@api.post("/api/story")
def generate_story(request: StoryRequest) -> dict:
    mode = resolve_mode(request.mode)
    model = resolve_model(request.model)

    try:
        if mode["id"] == "1":
            story = run_mode1_story(
                request, model=model, temperature=request.temperature, max_tokens=request.max_tokens
            )
        else:
            prompt = build_story_prompt(request, mode["id"])
            story = generate_with_openai(
                prompt=prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                model=model,
            )
    except RuntimeError as missing_key:
        raise HTTPException(status_code=400, detail=str(missing_key)) from missing_key
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"No se pudo generar el cuento: {err}") from err

    return {"story": story, "mode": mode["id"], "model": model}


@api.get("/api/options")
def list_options() -> dict:
    return {
        "models": AVAILABLE_MODELS,
        "defaultModel": DEFAULT_MODEL,
        "defaultMode": DEFAULT_MODE,
        "modes": MODES,
    }


@api.get("/api/experiments")
def list_experiment_payloads() -> dict:
    return {"experiments": get_experiments()}


api.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
