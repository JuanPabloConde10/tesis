from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional


class LLMClient(ABC):
    """Common interface for Large Language Model providers."""

    def __init__(self, model: str) -> None:
        self.model = model

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Return a complete response for the given prompt."""

    def stream(self, prompt: str, **kwargs) -> Iterable[str]:
        """Yield chunks for providers that support streaming."""
        raise NotImplementedError("Streaming is not implemented for this client.")

    def normalize_params(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> dict:
        """Standardize optional parameters across providers."""
        params: dict = {}
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        params.update(kwargs)
        return params
