import logging
import traceback
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from experiments.data import get_experiments
from infrastructure.llm_client import get_models
from infrastructure.llm_client.exceptions import LLMQuotaExceededError
from story_creator.modes import get_modes, generate_the_story
from axis_of_interest.registry import list_of_aoi
from .global_schemas import StoryRequest
from .constants import STRATEGIES, GENERATION_METHODS

load_dotenv()

logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parent
WEB_DIR = BASE_PATH.parent.parent / "web"

api = FastAPI(title="Taller de cuentos")

AVAILABLE_MODELS = get_models()
DEFAULT_MODEL = AVAILABLE_MODELS[0]

MODES = get_modes()
DEFAULT_MODE = MODES[0]["id"]
AOI_NAMES = sorted({aoi.name for aoi in list_of_aoi})


def resolve_model(model_name: Optional[str]) -> str:
    if model_name:
        if model_name not in AVAILABLE_MODELS:
            raise HTTPException(
                status_code=400, detail=f"Modelo no habilitado: {model_name}"
            )
        return model_name
    return DEFAULT_MODEL


def resolve_mode(mode_name: Optional[str]) -> dict:
    mode_id = mode_name or DEFAULT_MODE
    for mode in MODES:
        if mode["id"] == mode_id:
            return mode
    raise HTTPException(
        status_code=400, detail=f"Modo de creación desconocido: {mode_id}"
    )


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
        story = generate_the_story(request, mode_id=mode["id"])
    except RuntimeError as missing_key:
        raise HTTPException(status_code=400, detail=str(missing_key)) from missing_key
    except LLMQuotaExceededError as quota_err:
        raise HTTPException(status_code=429, detail=str(quota_err)) from quota_err
    except Exception as err:
        err_msg = str(err)
        if "401" in err_msg or "invalid_api_key" in err_msg or "Incorrect API key" in err_msg:
            logger.warning("API key inválida o rechazada: %s", err_msg[:200])
            raise HTTPException(
                status_code=401,
                detail="Clave de API de OpenAI inválida o revocada. Revisá OPENAI_API_KEY en .env y generá una nueva en https://platform.openai.com/account/api-keys",
            ) from err
        logger.exception(
            "Error generando cuento: %s\n%s", err, traceback.format_exc()
        )
        raise HTTPException(
            status_code=500, detail=f"No se pudo generar el cuento: {err}"
        ) from err

    return {"story": story, "mode": mode["id"], "model": model}


@api.get("/api/options")
def list_options() -> dict:
    return {
        "models": AVAILABLE_MODELS,
        "defaultModel": DEFAULT_MODEL,
        "defaultMode": DEFAULT_MODE,
        "modes": MODES,
        "aoiNames": AOI_NAMES,
        "strategies": STRATEGIES,
        "generationMethods": GENERATION_METHODS,
    }


@api.get("/api/experiments")
def list_experiment_payloads() -> dict:
    return {"experiments": get_experiments()}


api.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
