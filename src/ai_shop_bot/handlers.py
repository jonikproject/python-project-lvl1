from __future__ import annotations

import logging
from typing import Iterable

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .llm import ChatService

LOGGER = logging.getLogger(__name__)


WELCOME_TEXT = (
    "Привет! Я ваш AI-консультант магазина. Опишите, что вы ищете, и я помогу найти подходящий товар."
)
HELP_TEXT = (
    "Я могу подсказать, какие товары подойдут под ваши требования, рассказать о характеристиках "
    "и помочь сравнить варианты. Просто напишите, что вам нужно."
)


def register(application: Application, chat_service: ChatService) -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply(chat_service)))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: D401
    """Send a welcome message."""
    await update.message.reply_text(WELCOME_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: D401
    """Send help instructions."""
    await update.message.reply_text(HELP_TEXT)


def reply(chat_service: ChatService):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.message:
            return

        user_message = update.message.text
        if not user_message:
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        try:
            response = await chat_service.generate_reply(user_message, _extract_thread(context.chat_data))
        except Exception:  # pragma: no cover - defensive logging
            LOGGER.exception("Failed to generate reply")
            await update.message.reply_text("Извините, не получилось обработать запрос. Попробуйте ещё раз позже.")
            return

        _append_to_thread(context.chat_data, user_message)
        _append_to_thread(context.chat_data, response)
        await update.message.reply_text(response)

    return handler


def _extract_thread(chat_data: dict) -> Iterable[str]:
    return chat_data.get("history", [])


def _append_to_thread(chat_data: dict, entry: str) -> None:
    history = chat_data.setdefault("history", [])
    history.append(entry)
    if len(history) > 10:
        chat_data["history"] = history[-10:]
