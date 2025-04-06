import requests
import logging
from config import TINYURL_API_KEY

logger = logging.getLogger(__name__)

def shorten_url(url):
    logger.debug("Versuche URL zu kürzen: %s", url)

    if not TINYURL_API_KEY:
        logger.warning("Kein TinyURL API Key gefunden, gebe ursprüngliche URL zurück.")
        return url

    api_url = "https://api.tinyurl.com/create"
    headers = {
        "Authorization": f"Bearer {TINYURL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "url": url
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        short_url = response.json()["data"]["tiny_url"]
        logger.info("URL erfolgreich gekürzt: %s → %s", url, short_url)
        return short_url
    except Exception as e:
        logger.error("Fehler beim Kürzen der URL: %s", e, exc_info=True)
        return url
