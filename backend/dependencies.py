# dependencies.py
# Файл для создания и регистрации всех зависимостей: клиентов, сервисов, парсеров.
# Возвращает словарь (или кастомный DI-контейнер), который используется в других частях проекта.

from backend.clients.telegram_client import TelegramClient
from backend.clients.el_labs_client import ElevenLabsClient
from backend.parsers.news_parser import get_news_headlines
from backend.clients.gemini_client import get_gemini_response
from backend.prompts.news_prompts import build_prompt

def register_dependencies():
    container = {}

    container["news_parser"] = type("RssShim", (), {"get_headlines": staticmethod(get_news_headlines)})()
    container["telegram"] = TelegramClient()
    container["elevenlabs"] = ElevenLabsClient()
    container["gemini"] = get_gemini_response  # функция, не класс
    container["prompt_builder"] = build_prompt

    return container