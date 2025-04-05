import requests
from config import TELEGRAM_API_KEY, GROUP_ID

def send_message_to_topic(topic_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    params = {
        "chat_id": GROUP_ID,
        "text": message,
        "parse_mode": "Markdown",
        "message_thread_id": topic_id
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Failed to send Telegram message:", response.text)
