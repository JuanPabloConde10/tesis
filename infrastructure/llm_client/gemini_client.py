from typing import Dict, Optional

from google import genai

from .base import BaseLLMProvider, ChatMessage


class GeminiProvider(BaseLLMProvider):
    def __init__(self, client: genai.Client, model_id: str):
        self.client = client
        self.model_id = model_id

    def generate(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
    ) -> str:
        prompt = messages[-1]["content"]
        system_instruction = next(
            (m["content"] for m in messages if m["role"] == "system"), None
        )

        config: Dict[str, str | float] = {"temperature": temperature}
        if max_tokens is not None:
            config["max_output_tokens"] = max_tokens

        if system_instruction:
            config["system_instruction"] = system_instruction

        if stream:
            response = self.client.models.generate_content_stream(
                model=self.model_id,
                contents=prompt,
                config=config,
            )
            out = "".join(chunk.text or "" for chunk in response)
            return out
        else:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config,
            )
            return response.text or ""
