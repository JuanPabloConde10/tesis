import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

from experiments.data import get_experiments
from llm_client.models import get_models
from story_creator.modes import get_modes, generate_the_story
from global_schemas import StoryRequest

load_dotenv()

BASE_PATH = Path(__file__).parent
WEB_DIR = BASE_PATH / "web"

api = FastAPI(title="Taller de cuentos")

AVAILABLE_MODELS = get_models()
DEFAULT_MODEL = AVAILABLE_MODELS[0]

MODES = get_modes()
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
        story = generate_the_story(request)
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
