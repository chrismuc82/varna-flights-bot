import requests
import datetime
import logging
from config import KIWI_API_KEY

logger = logging.getLogger(__name__)

def fetch_flight_offers():
    logger.info("Starte Abruf von Flugangeboten.")

    url = "https://api.tequila.kiwi.com/v2/search"
    headers = {"accept": "application/json", "apikey": KIWI_API_KEY}

    today = datetime.datetime.today().strftime("%d/%m/%Y")
    three_months_later = (datetime.datetime.today() + datetime.timedelta(days=90)).strftime("%d/%m/%Y")
    one_months_later = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y")
    two_weeks_later = (datetime.datetime.today() + datetime.timedelta(days=14)).strftime("%d/%m/%Y")

    common_params = {
        "fly_from": "VAR",
        "fly_to": "DE",
        "date_from": today,
        "date_to": three_months_later,
        "curr": "EUR",
        "limit": 150,
        "sort": "price",
        "asc": 1,
        "locale": "de"  # Setzen der Sprache auf Deutsch
    }

    # One-way flights
    one_way_response = requests.get(url, headers=headers, params={**common_params, "return_from": "", "return_to": ""})
    if one_way_response.status_code == 200:
        logger.info("One-Way-Flüge erfolgreich abgerufen.")
        one_way_data = one_way_response.json()
        # Verarbeitung der One-Way-Flugdaten
    else:
        logger.error("Fehler beim Abrufen der One-Way-Flüge: %s", one_way_response.text)

    # Roundtrip flights
    roundtrip_response = requests.get(url, headers=headers, params={**common_params, "return_from": two_weeks_later, "return_to": one_months_later})
    if roundtrip_response.status_code == 200:
        logger.info("Roundtrip-Flüge erfolgreich abgerufen.")
        roundtrip_data = roundtrip_response.json()
        # Verarbeitung der Roundtrip-Flugdaten
    else:
        logger.error("Fehler beim Abrufen der Roundtrip-Flüge: %s", roundtrip_response.text)

    # Weitere Verarbeitung und Rückgabe der Daten
