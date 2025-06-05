from backend.prompts.news_prompts import BUNKER_INTRO
from backend.parsers.news_parser import get_news_headlines
from backend.clients.gemini_client import get_gemini_response
from backend.clients.telegram_client import send_telegram_message, send_telegram_audio
from backend.clients.el_labs_client import generate_audio_from_text

def job():
    news_info = get_news_headlines()
    prompt = f"{BUNKER_INTRO}\n\nLatest real headlines:\n{news_info}\n\nAdd in Pip-Boy style!"
    response = get_gemini_response(prompt)
    send_telegram_message(response)
    audio_file = generate_audio_from_text(response)
    if audio_file:
        send_telegram_audio(audio_file)

if __name__ == "__main__":
    print("Fallout Radio: Bunker-FM launched!")
    job()
