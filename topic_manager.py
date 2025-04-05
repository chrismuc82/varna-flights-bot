import requests
import json
import os
import random
from config import TELEGRAM_API_KEY, GROUP_ID

TOPICS_FILE = "topics.json"

VALID_TOPIC_COLORS = [
    7322096,     # Blue
    16766590,    # Red
    13338331,     # Green
    9367192,    # Orange
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
            except json.JSONDecodeError:
                return {}
    return {}


def save_topics(topics):
    with open(TOPICS_FILE, "w") as f:
        json.dump(topics, f, indent=2)


def create_topic(city_name):
    icon_color = get_random_icon_color()
    """Create a new topic in the Telegram group."""
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/createForumTopic"
    params = {
        "chat_id": GROUP_ID,
        "name": city_name,
        "icon_color": icon_color
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        topic_data = response.json()
        print("Create topic response:", topic_data)
        return topic_data["result"]["message_thread_id"]
    else:
        print(f"Failed to create topic for {city_name}: {response.text}")
        return None


def ensure_topic_exists(city, iata_code):
    """Ensure that a topic exists for the given city and IATA code. Returns topic_id."""
    topics = load_topics()

    if iata_code in topics:
        return topics[iata_code]["topic_id"]

    # Falls noch nicht vorhanden → neue Farbe auswählen und Topic anlegen
    icon_color = get_random_icon_color()
    topic_id = create_topic(city)

    if topic_id:
        topics[iata_code] = {
            "city": city,
            "topic_id": topic_id,
            "icon_color": icon_color
        }
        save_topics(topics)
        return topic_id
    else:
        return None
