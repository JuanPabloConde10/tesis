from typing import Optional, Literal, TypedDict, List


ProviderName = Literal["openai", "gemini", "local"]

SUPPORTED_PROVIDERS: frozenset[ProviderName] = frozenset({"openai", "gemini", "local"})


class ChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


def build_messages(prompt: str, system_prompt: Optional[str]) -> List[ChatMessage]:
    messages: List[ChatMessage] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


class BaseLLMProvider:
    def generate(
        self,
        messages: List[ChatMessage],
        *,
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
    ) -> str:
        raise NotImplementedError

