from __future__ import annotations

from typing import Iterable, Optional

from huggingface_hub import InferenceClient

from .base import LLMClient


class HuggingFaceHubClient(LLMClient):
    """Access models hosted on Hugging Face Hub Inference API."""

    def __init__(
        self,
        api_key: str,
        model: str = "mistralai/Mistral-7B-Instruct-v0.2",
    ) -> None:
        super().__init__(model=model)
        self._client = InferenceClient(model=model, token=api_key)

    def _normalize(self, **params) -> dict:
        normalized = self.normalize_params(**params)
        if "max_tokens" in normalized:
            normalized["max_new_tokens"] = normalized.pop("max_tokens")
        normalized.setdefault("return_full_text", False)
        return normalized

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        params = self._normalize(**kwargs)
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        return self._client.text_generation(
            prompt,
            **params,
        )

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterable[str]:
        params = self._normalize(**kwargs)
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        for chunk in self._client.text_generation(
            prompt,
            stream=True,
            **params,
        ):
            yield chunk
