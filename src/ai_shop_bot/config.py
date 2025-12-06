from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    telegram_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    system_prompt: str = (
        "You are an AI shopping assistant for a retail store. "
        "Provide concise, helpful answers and ask clarifying questions when needed."
    )

    @classmethod
    def from_env(cls) -> "Settings":
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not telegram_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is required")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is required")

        openai_model = os.getenv("OPENAI_MODEL", cls.openai_model)
        system_prompt = os.getenv("SYSTEM_PROMPT", cls.system_prompt)

        return cls(
            telegram_token=telegram_token,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            system_prompt=system_prompt,
        )
