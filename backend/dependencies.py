"""Dependency container configuration."""

from backend.clients.telegram_client import TelegramClient
from backend.clients.el_labs_client import ElevenLabsClient
from backend.clients.google_tts_client import GoogleTTSClient
from backend.parsers.news_parser import get_news_headlines
from backend.clients.gemini_client import get_gemini_response
from backend.prompts.news_prompts import build_prompt


def register_dependencies() -> dict:
    """Create and return dependency container."""

    container: dict[str, object] = {}

    container["news_parser"] = type(
        "RssShim",
        (),
        {"get_headlines": staticmethod(get_news_headlines)},
    )()
    container["telegram"] = TelegramClient()
    container["elevenlabs"] = ElevenLabsClient()
    container["google_tts"] = GoogleTTSClient()
    container["gemini"] = get_gemini_response  # function, not class
    container["prompt_builder"] = build_prompt

    return container

