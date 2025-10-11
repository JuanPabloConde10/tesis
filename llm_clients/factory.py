from __future__ import annotations

from typing import Optional

from config import Settings

from .anthropic_client import AnthropicClient
from .base import LLMClient
from .google_client import GoogleGenerativeAIClient
from .hf_client import HuggingFaceHubClient
from .openai_client import OpenAIClient

SUPPORTED_PROVIDERS = {"openai", "anthropic", "google", "huggingface"}


class MissingCredentialsError(RuntimeError):
    """Raised when the chosen provider is missing required credentials."""


def build_client(
    provider: Optional[str],
    settings: Settings,
) -> LLMClient:
    selected = (provider or settings.default_provider).lower()
    if selected not in SUPPORTED_PROVIDERS:
        readable = ", ".join(sorted(SUPPORTED_PROVIDERS))
        msg = f"Proveedor '{selected}' no soportado. Opciones: {readable}."
        raise ValueError(msg)

    if selected == "openai":
        if not settings.openai_api_key:
            raise MissingCredentialsError(
                "Falta definir OPENAI_API_KEY para usar el proveedor OpenAI."
            )
        return OpenAIClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    if selected == "anthropic":
        if not settings.anthropic_api_key:
            raise MissingCredentialsError(
                "Falta definir ANTHROPIC_API_KEY para usar el proveedor Anthropic."
            )
        return AnthropicClient(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
        )

    if selected == "google":
        if not settings.google_api_key:
            raise MissingCredentialsError(
                "Falta definir GOOGLE_API_KEY para usar el proveedor Google."
            )
        return GoogleGenerativeAIClient(
            api_key=settings.google_api_key,
            model=settings.google_model,
        )

    if not settings.huggingface_api_key:
        raise MissingCredentialsError(
            "Falta definir HUGGINGFACE_API_KEY para usar el proveedor Hugging Face."
        )
    return HuggingFaceHubClient(
        api_key=settings.huggingface_api_key,
        model=settings.huggingface_model,
    )
