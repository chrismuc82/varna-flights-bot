import requests
import random
import logging
from config import TELEGRAM_API_KEY, GROUP_ID
from remote_storage import load_topics, save_topics  # NEU

logger = logging.getLogger(__name__)

VALID_TOPIC_COLORS = [
    7322096,     # Blau
    16766590,    # Rot
    13338331,    # Grün
    9367192,     # Orange
    16749490,    # Lila
    16478047     # Pink
]


def get_random_icon_color():
    return random.choice(VALID_TOPIC_COLORS)


def create_topic(city_name):
    icon_color = get_random_icon_color()
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/createForumTopic"
    params = {
        "chat_id": GROUP_ID,
        "name": city_name,
        "icon_color": icon_color
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        topic_data = response.json()
        logger.info("Neues Topic erstellt für %s: %s", city_name, topic_data)
        return topic_data["result"]["message_thread_id"]
    else:
        logger.error("Fehler beim Erstellen eines Topics für %s: %s", city_name, response.text)
        return None


def ensure_topic_exists(city, iata_code):
    """Stellt sicher, dass es ein Topic für die gegebene Destination gibt."""
    topics = load_topics()

    if iata_code in topics:
        return topics[iata_code]["topic_id"]

    topic_id = create_topic(city)

    if topic_id:
        icon_color = get_random_icon_color()
        topics[iata_code] = {
            "city": city,
            "topic_id": topic_id,
            "icon_color": icon_color
        }
        save_topics(topics)
        return topic_id
    else:
        logger.warning("Topic konnte für %s (%s) nicht erstellt werden.", city, iata_code)
        return None