"""Simple Google Text-to-Speech client."""

import base64
import json
from typing import Optional

import requests

from backend.config.config import GEMINI_API_KEY


class GoogleTTSClient:
    """Generate speech audio using the Google generative TTS API."""

    def __init__(self, api_key: str = GEMINI_API_KEY) -> None:
        self.api_key = api_key

    def generate_audio(self, text: str, filename: str = "bunker_audio.mp3") -> Optional[str]:
        """Generate an MP3 file for the provided text.

        Parameters
        ----------
        text:
            The text to convert to speech.
        filename:
            The file to write the MP3 data into.

        Returns
        -------
        str | None
            Path to the generated file or ``None`` if generation failed.
        """

        if not self.api_key:
            print("Google TTS API key not provided, skipping audio generation")
            return None

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.5-flash-preview-tts:generateContent?key={self.api_key}"
        )

        payload = {
            "input": {"text": text},
            "voice": {"languageCode": "ru-RU", "name": "ru-RU-Standard-A"},
            "audioConfig": {"audioEncoding": "MP3"},
        }

        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            audio_content = response.json().get("audioContent")
            if not audio_content:
                print("⚠️ Google TTS returned no audio content")
                return None
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(audio_content))
            return filename
        except Exception as exc:
            print(f"Error during Google TTS request: {exc}")
            return None

