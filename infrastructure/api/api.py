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
from infrastructure.llm_client import get_client
from story_creator.modes import get_modes, generate_the_story, generate_story_candidates
from evaluation import evaluate_generated_story_dimensions, rank_candidates
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
    request_payload = request.model_copy(update={"mode": mode["id"], "model": model})
    try:
        num_candidates = request_payload.num_candidates or 1
        selection_policies = request_payload.selection_policies or []

        if num_candidates > 1 and not selection_policies:
            selection_policies = ["mean"]

        if num_candidates == 1 and not selection_policies:
            story = generate_the_story(request_payload, mode_id=mode["id"])
            response = {"story": story, "mode": mode["id"], "model": model}
            if isinstance(story, tuple):
                story_text, plot_schema = story
                response["story"] = story_text
                response["plot_schema"] = plot_schema
            return response

        candidates = generate_story_candidates(
            request_payload,
            mode_id=mode["id"],
            num_candidates=num_candidates,
        )
        judge_client = get_client(model)

        evaluated_candidates = []
        for candidate in candidates:
            evaluation = evaluate_generated_story_dimensions(
                candidate["story"],
                judge_client,
                metadata={"mode": mode["id"], "candidate_id": candidate["candidate_id"]},
            )
            evaluated_candidates.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "story": candidate["story"],
                    "plot_schema": candidate.get("plot_schema"),
                    "evaluation": evaluation,
                }
            )

        ranking = rank_candidates(
            evaluated_candidates,
            policies=selection_policies,
            weighted_policy_weights=request_payload.weighted_policy_weights,
        )
        primary_policy = ranking["policies"][0]
        primary_winner = ranking["winners"][primary_policy]

        selected_stories_by_policy = {
            policy: winner["story"] for policy, winner in ranking["winners"].items()
        }
        winner_metadata_by_policy = {
            policy: {
                "candidate_id": winner["candidate_id"],
                "policy_score": winner["policy_score"],
                "dimensions": winner["evaluation"]["dimensions"],
            }
            for policy, winner in ranking["winners"].items()
        }

        response = {
            "story": primary_winner["story"],
            "mode": mode["id"],
            "model": model,
            "num_candidates": num_candidates,
            "selection_policies": ranking["policies"],
            "weighted_policy_weights_normalized": ranking.get(
                "weighted_policy_weights_normalized"
            ),
            "selected_stories_by_policy": selected_stories_by_policy,
            "winner_metadata_by_policy": winner_metadata_by_policy,
            "rankings": ranking["rankings"],
            "candidates": [
                {
                    "candidate_id": candidate["candidate_id"],
                    "story": candidate["story"],
                    "plot_schema": candidate.get("plot_schema"),
                    "dimensions": candidate["evaluation"]["dimensions"],
                    "average_score": candidate["evaluation"]["average_score"],
                    "justification": candidate["evaluation"].get("justification", ""),
                }
                for candidate in evaluated_candidates
            ],
        }
        if primary_winner.get("plot_schema") is not None:
            response["plot_schema"] = primary_winner["plot_schema"]
        return response
    except ValueError as validation_error:
        raise HTTPException(status_code=400, detail=str(validation_error)) from validation_error
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


@api.get("/api/aois")
def list_aois() -> dict:
    """Lista todos los Axis of Interest disponibles."""
    from axis_of_interest.registry import list_of_aoi
    
    aois = [
        {
            "id": aoi.id,
            "name": aoi.name,
            "description": aoi.description,
            "roles": aoi.roles,
        }
        for aoi in list_of_aoi
    ]
    
    strategies = [
        {"id": "sequential", "name": "Sequential", "description": "Concatena todos los spans en orden"},
        {"id": "round_robin", "name": "Round Robin", "description": "Alterna entre AOIs circularmente"},
        {"id": "parallel", "name": "Parallel", "description": "Agrupa spans por posición"},
        {"id": "random", "name": "Random", "description": "Selección aleatoria respetando orden interno"},
        {"id": "llm", "name": "LLM", "description": "El LLM decide el orden completo"},
    ]
    
    return {"aois": aois, "strategies": strategies}


api.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
