from pathlib import Path
from typing import Optional
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openai import OpenAI

load_dotenv()

BASE_PATH = Path(__file__).parent
WEB_DIR = BASE_PATH / "web"

api = FastAPI(title="Taller de cuentos")

ARC_LABELS = {
    "viaje_del_heroe": "Viaje del héroe",
    "maduracion": "Historia de maduración",
    "busqueda": "Búsqueda",
    "venganza": "Venganza",
    "comedia_de_enredos": "Comedia de enredos",
    "tragedia": "Tragedia",
}


class StoryRequest(BaseModel):
    trama: str = Field(..., min_length=5)
    genero: Optional[str] = None
    arco: Optional[str] = None
    personajes: list[str] = Field(default_factory=list)
    temperature: Optional[float] = Field(default=None, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)


def build_story_prompt(data: StoryRequest) -> str:
    personajes = ", ".join(data.personajes) if data.personajes else "No especificados"
    genero = data.genero or "Libre"
    arco = ARC_LABELS.get(data.arco, data.arco) if data.arco else "Libre"
    return (
        "Escribe un cuento breve en español usando los datos proporcionados.\n"
        f"- Descripción de la trama: {data.trama}\n"
        f"- Personajes principales: {personajes}\n"
        f"- Género: {genero}\n"
        f"- Arco narrativo: {arco}\n\n"
        "Extensión: 3 a 5 párrafos. Mantén un tono acorde al género y cierra con un desenlace claro. "
        "Responde solo con el cuento."
    )


def generate_with_openai(prompt: str, temperature: Optional[float], max_tokens: Optional[int]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")

    model = os.getenv("OPENAI_MODEL", "gpt-5-mini-2025-08-07")
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
    prompt = build_story_prompt(request)

    try:
        story = generate_with_openai(
            prompt=prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except RuntimeError as missing_key:
        raise HTTPException(status_code=400, detail=str(missing_key)) from missing_key
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"No se pudo generar el cuento: {err}") from err

    return {"story": story}


api.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
