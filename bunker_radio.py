import asyncio
from backend.dependencies import register_dependencies
from backend.core.fallout_news_logic import run_bunker_sequence

container = register_dependencies()

def job():
    headlines, response = asyncio.run(run_bunker_sequence(container))
    telegram = container["telegram"]
    elevenlabs = container["elevenlabs"]
    telegram.send_message(response)
    audio_file = elevenlabs.generate_audio(response)
    if audio_file:
        telegram.send_audio(audio_file)

if __name__ == "__main__":
    print("Fallout Radio: Bunker-FM launched!")
    job()
