import requests
import json
import os
import random
import logging
from config import TELEGRAM_API_KEY, GROUP_ID

logger = logging.getLogger(__name__)

TOPICS_FILE = "topics.json"

VALID_TOPIC_COLORS = [
    7322096,     # Blue
    16766590,    # Red
    13338331,    # Green
    9367192,     # Orange
    16749490,    # Purple
    16478047     # Pink
]

def get_random_icon_color():
    return random.choice(VALID_TOPIC_COLORS)

def load_topics():
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning("JSON decode error when loading topics: %s", e)
                return {}
    return {}

def save_topics(topics):
    try:
        with open(TOPICS_FILE, "w") as f:
            json.dump(topics, f, indent=2)
        logger.info("Topics saved to %s", TOPICS_FILE)
    except Exception as e:
        logger.error("Failed to save topics to %s: %s", TOPICS_FILE, e, exc_info=True)

def create_topic(city_name):
    icon_color = get_random_icon_color()
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/createForumTopic"
    params = {
        "chat_id": GROUP_ID,
        "name": city_name,
        "icon_color": icon_color
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        topic_data = response.json()
        logger.info("Created topic for %s: %s", city_name, topic_data)
        return topic_data["result"]["message_thread_id"]
    except Exception as e:
        logger.error("Failed to create topic for %s: %s", city_name, e, exc_info=True)
        return None

def ensure_topic_exists(city, iata_code):
    topics = load_topics()

    if iata_code in topics:
        return topics[iata_code]["topic_id"]

    topic_id = create_topic(city)
    if topic_id:
        topics[iata_code] = {
            "city": city,
            "topic_id": topic_id,
            "icon_color": get_random_icon_color()
        }
        save_topics(topics)
        logger.info("New topic created and stored for %s (%s)", city, iata_code)
        return topic_id
    else:
        logger.warning("Could not create or retrieve topic for %s (%s)", city, iata_code)
        return None
