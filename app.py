from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import settings
from infrastructure.llm_clients import build_client
from infrastructure.llm_clients.factory import MissingCredentialsError, SUPPORTED_PROVIDERS

app = FastAPI(title="LLM Playground")

app.mount("/static", StaticFiles(directory="web/static"), name="static")


class ChatRequest(BaseModel):
    prompt: str | None = None
    provider: str | None = None
    system: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    messages: list[dict[str, str]] | None = None


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse("web/index.html")


@app.get("/api/providers")
def get_providers() -> dict:
    return {
        "providers": sorted(SUPPORTED_PROVIDERS),
        "default": settings.default_provider,
    }


@app.post("/api/chat")
def create_chat(request: ChatRequest) -> dict:
    try:
        client = build_client(provider=request.provider, settings=settings)
    except MissingCredentialsError as credentials_error:
        raise HTTPException(status_code=400, detail=str(credentials_error)) from credentials_error
    except ValueError as invalid_provider:
        raise HTTPException(status_code=400, detail=str(invalid_provider)) from invalid_provider

    params: dict = {}
    if request.temperature is not None:
        params["temperature"] = request.temperature
    if request.max_tokens is not None:
        params["max_completion_tokens"] = request.max_tokens

    try:
        # Manejar formato de mensajes (nuevo)
        if request.messages:
            # Convertir mensajes a prompt y system
            system_messages = [msg for msg in request.messages if msg.get("role") == "system"]
            
            # Construir prompt con contexto
            prompt_parts = []
            
            # Agregar mensaje de sistema si existe
            if system_messages:
                prompt_parts.append(f"Sistema: {system_messages[0]['content']}")
                prompt_parts.append("")
            
            # Agregar historial de conversación
            all_messages = sorted(request.messages, key=lambda x: request.messages.index(x))
            for msg in all_messages:
                if msg["role"] == "system":
                    continue  # Ya lo agregamos arriba
                role_name = "Usuario" if msg["role"] == "user" else "Asistente"
                prompt_parts.append(f"{role_name}: {msg['content']}")
            
            final_prompt = "\n".join(prompt_parts)
            system_prompt = system_messages[0]["content"] if system_messages else None
            
            response = client.generate(
                final_prompt,
                system_prompt=system_prompt,
                **params,
            )
        else:
            # Formato antiguo (compatible)
            if not request.prompt:
                raise HTTPException(status_code=400, detail="Se requiere 'prompt' o 'messages'")
            
            response = client.generate(
                request.prompt,
                system_prompt=request.system,
                **params,
            )
    except Exception as err:  # pragma: no cover - defensive against provider errors
        raise HTTPException(status_code=500, detail=f"Error al generar respuesta: {err}") from err

    return {"response": response}
