import json
import os
import requests
from config import TELEGRAM_API_KEY, GROUP_ID

TOPICS_FILE = "topics.json"


def load_topics():
    """Lädt die gespeicherten Topics oder gibt ein leeres Dictionary zurück, falls die Datei leer oder ungültig ist."""
    if not os.path.exists(TOPICS_FILE):  # Falls die Datei nicht existiert, erstelle eine leere Datei
        save_topics({})
        return {}

    try:
        with open(TOPICS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}  # Falls die Datei leer ist, return {}
    except json.JSONDecodeError:
        print("Fehler: Die Datei topics.json ist beschädigt. Sie wird zurückgesetzt.")
        save_topics({})
        return {}


def save_topics(topics):
    """Save topics to the file."""
    with open(TOPICS_FILE, "w") as f:
        json.dump(topics, f)


def create_topic(topic_name):
    """Create a new topic in the Telegram group."""
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/createForumTopic"
    response = requests.get(url, params={"chat_id": GROUP_ID, "name": topic_name})

    if response.status_code == 200:
        topic_data = response.json()
        print("Create topic response:", topic_data)  # Debugging output

        # Fix: Use "message_thread_id" instead of "topic_id"
        if "result" in topic_data and "message_thread_id" in topic_data["result"]:
            return topic_data["result"]["message_thread_id"]
        else:
            print(f"Failed to extract topic ID: {topic_data}")
            return None  # Handle missing message_thread_id
    else:
        print(f"Failed to create topic: {response.text}")
        return None


def ensure_topic_exists(city, iata_code):
    """Ensure that the topic exists for a given city. Create it if necessary."""
    topics = load_topics()

    # Check if the topic exists using IATA code as the key
    if iata_code in topics:
        return topics[iata_code]["topic_id"]

    # If the topic does not exist, create it
    new_topic_id = create_topic(city)
    if new_topic_id:
        topics[iata_code] = {
            "city_name": city,
            "topic_id": new_topic_id
        }
        save_topics(topics)
        return new_topic_id
    else:
        return None