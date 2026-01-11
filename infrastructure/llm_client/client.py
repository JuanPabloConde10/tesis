import os
from typing import Optional

from openai import OpenAI
from google import genai

from .base import build_messages, BaseLLMProvider, ProviderName, SUPPORTED_PROVIDERS
from .openai_client import OpenAIProvider
from .gemini_client import GeminiProvider
from .utils import DEFAULT_LOCAL_BASE_URL


class ClientLLM:
    """Facade cliente para distintos proveedores de LLM.

    La implementación concreta de cada proveedor está separada en módulos
    (`openai_client.py`, `gemini_client.py`). Esto mantiene `client.py` corto
    y fácil de mantener.
    """

    def __init__(
        self,
        *,
        provider: ProviderName,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Proveedor no soportado: {provider}")

        self.provider = provider
        self.model = model
        self.provider_impl = self._resolve_provider(
            provider=provider, model=model, api_key=api_key, base_url=base_url
        )

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> str:
        messages = build_messages(prompt, system_prompt)

        return self.provider_impl.generate(
            messages, temperature=temperature, max_tokens=max_tokens, stream=stream
        )

    def _resolve_provider(
        self,
        *,
        provider: ProviderName,
        model: str,
        api_key: Optional[str],
        base_url: Optional[str],
    ) -> BaseLLMProvider:
        if provider == "openai":
            key = api_key or os.getenv("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("Falta OPENAI_API_KEY")

            client_kwargs = {"api_key": key}
            resolved_base = base_url or os.getenv("OPENAI_BASE_URL")
            if resolved_base:
                client_kwargs["base_url"] = resolved_base

            client = OpenAI(**client_kwargs)
            return OpenAIProvider(client, model)

        if provider == "local":
            resolved_base = (
                base_url
                or os.getenv("LMSTUDIO_BASE_URL")
                or os.getenv("LOCAL_LLM_BASE_URL")
                or DEFAULT_LOCAL_BASE_URL
            )
            token = (
                api_key
                or os.getenv("LMSTUDIO_API_KEY")
                or os.getenv("LOCAL_LLM_API_KEY")
                or "lm-studio"
            )

            client = OpenAI(api_key=token, base_url=resolved_base)
            return OpenAIProvider(client, model)

        if provider == "gemini":
            key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not key:
                raise RuntimeError("Falta GEMINI_API_KEY o GOOGLE_API_KEY")
            client = genai.Client(api_key=key)
            return GeminiProvider(client, model)

        raise ValueError(f"Proveedor no soportado: {provider}")
