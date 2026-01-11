from typing import Optional
from openai import OpenAI

from .base import BaseLLMProvider, ChatMessage


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def generate(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
    ) -> str:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**kwargs)

        if stream:
            return "".join(chunk.choices[0].delta.content or "" for chunk in response)

        return response.choices[0].message.content or ""
