from __future__ import annotations

from typing import Iterable, Optional

from openai import OpenAI

from .base import LLMClient


class OpenAIClient(LLMClient):
    """Thin wrapper around the OpenAI Chat Completions API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
    ) -> None:
        super().__init__(model=model)
        self._client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        params = self.normalize_params(**kwargs)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            **params,
        )
        return response.choices[0].message.content or ""

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterable[str]:
        params = self.normalize_params(**kwargs)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **params,
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if not delta:
                continue
            content = getattr(delta, "content", None)
            if not content:
                continue
            if isinstance(content, str):
                yield content
            else:
                for part in content:
                    if getattr(part, "type", None) == "text" and getattr(
                        part, "text", None
                    ):
                        yield part.text
