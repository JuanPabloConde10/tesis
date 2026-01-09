import os
from typing import Iterable, Optional

import google.generativeai as genai
from openai import OpenAI

SUPPORTED_PROVIDERS = {"openai", "gemini", "local", "lmstudio"}
DEFAULT_LOCAL_BASE_URL = "http://localhost:1234/v1"


class Client_llm:
    """
    Cliente unificado para distintos proveedores de LLM.

    Ejemplo de uso:
        client = Client_llm("gpt-4o-mini", provider="openai")
        texto = client.generate("Contame un cuento corto.")
    """

    def __init__(
        self,
        modelo: str,
        provider: str,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.model = modelo
        normalized = provider.lower()
        # Permitimos alias explícito para LM Studio.
        self.provider = "local" if normalized == "lmstudio" else normalized
        if self.provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Proveedor no soportado: {provider}")
        self.base_url = base_url
        self.api_key = api_key or self._get_default_api_key()
        self.client = resolve_client(
            self.provider, self.model, base_url=self.base_url, api_key=self.api_key
        )

    def _get_default_api_key(self) -> Optional[str]:
        if self.provider == "openai":
            return os.getenv("OPENAI_API_KEY")
        if self.provider == "gemini":
            return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if self.provider == "local":
            return (
                os.getenv("LMSTUDIO_API_KEY")
                or os.getenv("LOCAL_LLM_API_KEY")
                or os.getenv("HUGGINGFACEHUB_API_TOKEN")
                or "lm-studio"
            )
        return None

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> str:
        if self.provider == "openai":
            return _generate_with_openai(
                self.client,
                model=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
        if self.provider == "gemini":
            return _generate_with_gemini(
                self.client,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
        if self.provider == "local":
            return _generate_with_openai(
                self.client,
                model=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )
        raise ValueError(f"Proveedor no soportado: {self.provider}")


def resolve_client(
    provider: str,
    modelo: str,
    *,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Devuelve el cliente concreto según el proveedor."""
    normalized = provider.lower()
    if normalized == "openai":
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable OPENAI_API_KEY")
        client_kwargs = {"api_key": api_key}
        resolved_base = base_url or os.getenv("OPENAI_BASE_URL")
        if resolved_base:
            client_kwargs["base_url"] = resolved_base
        return OpenAI(**client_kwargs)

    if normalized == "gemini":
        api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable GEMINI_API_KEY o GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(modelo)

    if normalized == "local":
        # LM Studio expone una API compatible con OpenAI.
        resolved_base = (
            base_url or os.getenv("LMSTUDIO_BASE_URL") or os.getenv("LOCAL_LLM_BASE_URL") or DEFAULT_LOCAL_BASE_URL
        )
        token = api_key or os.getenv("LMSTUDIO_API_KEY") or os.getenv("LOCAL_LLM_API_KEY") or "lm-studio"
        return OpenAI(api_key=token, base_url=resolved_base)

    raise ValueError(f"Proveedor no soportado: {provider}")


def _generate_with_openai(
    client: OpenAI,
    *,
    model: str,
    prompt: str,
    system_prompt: Optional[str],
    temperature: float,
    max_tokens: Optional[int],
    stream: bool,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    completion_kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
    }
    if max_tokens is not None:
        completion_kwargs["max_tokens"] = max_tokens

    response = client.chat.completions.create(**completion_kwargs)
    if stream:
        return "".join(chunk.choices[0].delta.content or "" for chunk in response)
    return response.choices[0].message.content or ""


def _generate_with_gemini(
    model: genai.GenerativeModel,
    *,
    prompt: str,
    system_prompt: Optional[str],
    temperature: float,
    max_tokens: Optional[int],
    stream: bool,
) -> str:
    contents: Iterable[str] | str = prompt
    if system_prompt:
        contents = [system_prompt, prompt]

    generation_config = {"temperature": temperature}
    if max_tokens is not None:
        generation_config["max_output_tokens"] = max_tokens

    response = model.generate_content(
        contents,
        generation_config=generation_config,
        stream=stream,
    )

    if stream:
        return "".join(part.text or "" for part in response)
    return response.text or ""
