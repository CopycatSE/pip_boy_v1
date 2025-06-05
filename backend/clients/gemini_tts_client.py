

# This script takes text from Gemini and uses Google Cloud TTS API to synthesize speech

import requests
import json
import base64
from config import GEMINI_API_KEY

def gemini_text_to_speech(text, output_path="output.mp3"):
    # Using Gemini 2.5 Flash Preview model with TTS endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Wavenet-D"  # You can change the voice model here
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        audio_content = response_json.get("audioContent")
        if audio_content:
            with open(output_path, "wb") as out:
                out.write(base64.b64decode(audio_content))
            print(f"✅ Audio content written to {output_path}")
        else:
            print("⚠️ No audio content returned.")
    except Exception as e:
        print(f"❌ Error during TTS request: {e}")