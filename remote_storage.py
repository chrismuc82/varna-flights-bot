import requests
import os
import json
import logging
from config import GIST_ID, GIST_TOKEN

logger = logging.getLogger(__name__)

GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

HEADERS = {
    "Authorization": f"token {GIST_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def load_file(filename):
    try:
        response = requests.get(GIST_API_URL, headers=HEADERS)
        if response.status_code == 200:
            files = response.json().get("files", {})
            if filename in files:
                content = files[filename]["content"]
                logger.info("%s erfolgreich aus Gist geladen.", filename)
                return json.loads(content)
            else:
                logger.warning("Datei %s nicht im Gist gefunden. Leere Struktur wird verwendet.", filename)
                return {}
        else:
            logger.error("Fehler beim Laden des Gists: %s", response.text)
            return {}
    except Exception as e:
        logger.exception("Unerwarteter Fehler beim Laden von %s: %s", filename, str(e))
        return {}

def save_file(filename, data):
    try:
        payload = {
            "files": {
                filename: {
                    "content": json.dumps(data, indent=2)
                }
            }
        }
        response = requests.patch(GIST_API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            logger.info("%s erfolgreich im Gist gespeichert.", filename)
        else:
            logger.error("Fehler beim Speichern von %s im Gist: %s", filename, response.text)
    except Exception as e:
        logger.exception("Unerwarteter Fehler beim Speichern von %s: %s", filename, str(e))


def load_topics():
    return load_file("topics.json")

def save_topics(topics):
    save_file("topics.json", topics)

def load_prices():
    return load_file("prices.json")

def save_prices(prices):
    save_file("prices.json", prices)
