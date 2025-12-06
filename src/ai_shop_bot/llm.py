from __future__ import annotations

import asyncio
from typing import Iterable

from openai import OpenAI

from .config import Settings


class ChatService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)

    async def generate_reply(self, prompt: str, context: Iterable[str] | None = None) -> str:
        messages = [{"role": "system", "content": self.settings.system_prompt}]
        if context:
            for entry in context:
                messages.append({"role": "user", "content": entry})

        messages.append({"role": "user", "content": prompt})

        response = await asyncio.to_thread(
            self._client.chat.completions.create,
            model=self.settings.openai_model,
            messages=messages,
            temperature=0.6,
        )

        return response.choices[0].message.content.strip()
