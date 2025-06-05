import requests
from backend.config.config import ELEVENLABS_API_KEY, VOICE_ID

class ElevenLabsClient:
    def __init__(self, api_key=ELEVENLABS_API_KEY, voice_id=VOICE_ID):
        self.api_key = api_key
        self.voice_id = voice_id

    def generate_audio(self, text, filename='bunker_audio.mp3'):
        if not self.api_key or not self.voice_id:
            print("ElevenLabs credentials not provided, skipping audio generation")
            return None
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.7,
                "speed": 1.15
            }
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error while creating audio: {e}")
            return None
