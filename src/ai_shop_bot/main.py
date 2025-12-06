from __future__ import annotations

import asyncio
import logging

from telegram.ext import Application

from .config import Settings
from .handlers import register
from .llm import ChatService

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)


async def main() -> None:
    settings = Settings.from_env()
    chat_service = ChatService(settings)

    application = Application.builder().token(settings.telegram_token).build()
    register(application, chat_service)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    try:
        await application.updater.wait_for_stop()
    finally:
        await application.stop()
        await application.shutdown()


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
