from __future__ import annotations

from typing import Iterable, Optional

import google.generativeai as genai

from .base import LLMClient


class GoogleGenerativeAIClient(LLMClient):
    """Interface for Google's Gemini models."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
    ) -> None:
        super().__init__(model=model)
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    def _build_generation_config(self, **params) -> dict:
        config: dict = {}
        if "temperature" in params:
            config["temperature"] = params.pop("temperature")
        if "max_tokens" in params:
            config["max_output_tokens"] = params.pop("max_tokens")
        config.update(params)
        return config

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        params = self.normalize_params(**kwargs)
        generation_config = self._build_generation_config(**params)
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        response = self._model.generate_content(
            prompt,
            generation_config=generation_config or None,
        )
        return response.text or ""

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterable[str]:
        params = self.normalize_params(**kwargs)
        generation_config = self._build_generation_config(**params)
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        response = self._model.generate_content(
            prompt,
            generation_config=generation_config or None,
            stream=True,
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
