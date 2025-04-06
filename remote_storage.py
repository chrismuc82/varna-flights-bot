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

def load_file_from_gist(filename):
    try:
        response = requests.get(GIST_API_URL, headers=HEADERS)
        if response.status_code == 200:
            files = response.json().get("files", {})
            if filename in files:
                content = files[filename]["content"]
                logger.info("Datei %s erfolgreich aus Gist geladen.", filename)
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

def save_file_to_gist(filename, content_dict):
    try:
        payload = {
            "files": {
                filename: {
                    "content": json.dumps(content_dict, indent=2)
                }
            }
        }
        response = requests.patch(GIST_API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            logger.info("Datei %s erfolgreich im Gist gespeichert.", filename)
        else:
            logger.error("Fehler beim Speichern der Datei %s im Gist: %s", filename, response.text)
    except Exception as e:
        logger.exception("Unerwarteter Fehler beim Speichern von %s: %s", filename, str(e))

def load_topics():
    return load_file_from_gist("topics.json")

def save_topics(topics):
    save_file_to_gist("topics.json", topics)
