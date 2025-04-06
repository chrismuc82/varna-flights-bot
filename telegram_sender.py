import requests
import logging
from config import TELEGRAM_API_KEY, GROUP_ID

logger = logging.getLogger(__name__)

def send_message_to_topic(topic_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    params = {
        "chat_id": GROUP_ID,
        "text": message,
        "parse_mode": "Markdown",
        "message_thread_id": topic_id
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.info("Nachricht erfolgreich an Topic %s gesendet.", topic_id)
    except requests.RequestException as e:
        logger.error("Fehler beim Senden der Nachricht an Topic %s: %s", topic_id, e, exc_info=True)
