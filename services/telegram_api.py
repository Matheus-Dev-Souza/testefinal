import os
import requests

class TelegramAPI:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}"

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=payload)
        response.raise_for_status()
