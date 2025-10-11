from __future__ import annotations

from typing import Iterable, Optional

from anthropic import Anthropic

from .base import LLMClient


class AnthropicClient(LLMClient):
    """Handle requests to Anthropic's Claude models."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-sonnet-20240229",
    ) -> None:
        super().__init__(model=model)
        self._client = Anthropic(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        params = self.normalize_params(**kwargs)
        if "max_tokens" in params:
            params["max_output_tokens"] = params.pop("max_tokens")
        response = self._client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            **params,
        )
        return "".join(block.text for block in response.content if block.type == "text")

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterable[str]:
        params = self.normalize_params(**kwargs)
        if "max_tokens" in params:
            params["max_output_tokens"] = params.pop("max_tokens")
        with self._client.messages.stream(
            model=self.model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            **params,
        ) as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    delta = event.delta
                    if getattr(delta, "type", None) == "text_delta" and delta.text:
                        yield delta.text
