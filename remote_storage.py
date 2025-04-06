import requests
import os
import json
import logging
from config import GIST_ID, GIST_TOKEN

logger = logging.getLogger(__name__)

FILENAME = "topics.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

HEADERS = {
    "Authorization": f"token {GIST_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def load_topics():
    try:
        response = requests.get(GIST_API_URL, headers=HEADERS)
        if response.status_code == 200:
            files = response.json().get("files", {})
            if FILENAME in files:
                content = files[FILENAME]["content"]
                logger.info("Topics erfolgreich aus Gist geladen.")
                return json.loads(content)
            else:
                logger.warning("Datei %s nicht im Gist gefunden. Leere Struktur wird verwendet.", FILENAME)
                return {}
        else:
            logger.error("Fehler beim Laden des Gists: %s", response.text)
            return {}
    except Exception as e:
        logger.exception("Unerwarteter Fehler beim Laden von Topics: %s", str(e))
        return {}


def save_topics(topics):
    try:
        payload = {
            "files": {
                FILENAME: {
                    "content": json.dumps(topics, indent=2)
                }
            }
        }
        response = requests.patch(GIST_API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            logger.info("Topics erfolgreich im Gist gespeichert.")
        else:
            logger.error("Fehler beim Speichern im Gist: %s", response.text)
    except Exception as e:
        logger.exception("Unerwarteter Fehler beim Speichern von Topics: %s", str(e))