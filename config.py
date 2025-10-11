from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Container for environment-driven configuration."""

    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")

    default_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()

    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    google_model: str = os.getenv("GOOGLE_MODEL", "gemini-pro")
    huggingface_model: str = os.getenv(
        "HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2"
    )


settings = Settings()
