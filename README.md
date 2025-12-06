# AI Shopping Consultant Telegram Bot

Этот проект содержит минимальный пример Telegram-бота на Python, который использует OpenAI для ответа на вопросы покупателей магазина.

## Возможности
- Команда `/start` — приветствие и краткое описание возможностей бота.
- Команда `/help` — подсказка, как формулировать запросы.
- Ответы на любые текстовые сообщения с использованием OpenAI Chat Completions.
- Сохранение короткой истории диалога для более контекстных ответов.

## Быстрый старт
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Подготовьте переменные окружения:
   - `TELEGRAM_BOT_TOKEN` — токен бота из BotFather.
   - `OPENAI_API_KEY` — ключ OpenAI.
   - Необязательно: `OPENAI_MODEL` (по умолчанию `gpt-4o-mini`) и `SYSTEM_PROMPT` для настройки тона бота.
3. Запустите бота (предполагается, что вы находитесь в корне репозитория):
   ```bash
   PYTHONPATH=src python -m ai_shop_bot.main
   ```

Бот будет использовать long polling и начнет отвечать на входящие сообщения.

## Структура
- `src/ai_shop_bot/config.py` — загрузка настроек из переменных окружения.
- `src/ai_shop_bot/llm.py` — обертка над OpenAI Chat Completions.
- `src/ai_shop_bot/handlers.py` — обработчики команд и сообщений Telegram.
- `src/ai_shop_bot/main.py` — сборка и запуск приложения.
