import requests
from backend.config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramClient:
    def __init__(self, token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text):
        if not self.token or not self.chat_id:
            print("Telegram credentials not provided, skipping send_message")
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {'chat_id': self.chat_id, 'text': text}
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending message to Telegram: {e}")

    def send_audio(self, audio_path):
        if not self.token or not self.chat_id:
            print("Telegram credentials not provided, skipping send_audio")
            return
        url = f"https://api.telegram.org/bot{self.token}/sendAudio"
        try:
            with open(audio_path, 'rb') as audio_file:
                files = {'audio': audio_file}
                data = {'chat_id': self.chat_id, 'title': 'Bunker-FM'}
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
        except Exception as e:
            print(f"Error sending audio to Telegram: {e}")
