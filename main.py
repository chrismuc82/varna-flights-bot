import requests
from collections import defaultdict
from flight_search import fetch_flight_offers, extract_flights_id
from topic_manager import ensure_topic_exists
from config import TELEGRAM_API_KEY, GROUP_ID
from telegram_formatter import format_flight_offer
import logging
from remote_storage import load_file, save_file  # Importiere die Funktionen aus remote_storage
from urllib.parse import urlparse, parse_qs

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Gist-Dateiname für die gespeicherten Preise
PRICE_FILENAME = "prices.json"

def compare_and_update_prices(current_offer, saved_prices):
    flight_id = extract_flights_id(current_offer["link"])  # Extract 'flightsId' from the 'link' field
    logger.debug(f"Vergleiche Angebot: {current_offer}")  # Log the current offer for debugging

    if flight_id:
        existing_offer = saved_prices.get(flight_id)

        if existing_offer:
            if current_offer["price"] < existing_offer["price"]:
                logger.info(f"Neues günstigeres Angebot für {current_offer['city']}: {current_offer['price']} EUR")
                saved_prices[flight_id] = current_offer  # Update the price if it's lower
                return current_offer, saved_prices  # Return the new offer

            elif current_offer["price"] == existing_offer["price"]:
                # Compare by departure date as well if prices are the same
                if current_offer["departure_time"] != existing_offer["departure_time"]:
                    logger.info(f"Angebot für {current_offer['city']} hat das Datum geändert.")
                    saved_prices[flight_id] = current_offer  # Update the saved prices with the new offer
                    return current_offer, saved_prices
        else:
            logger.info(f"Neues Angebot für {current_offer['city']} gefunden.")
            saved_prices[flight_id] = current_offer  # Add the new offer if it doesn't exist
            return current_offer, saved_prices  # Return the new offer

    else:
        logger.warning("Flugangebot hat keine gültige flightsId. Ignoriere das Angebot.")
        return None, saved_prices  # Return None if there is no valid 'flightsId'

    return None, saved_prices  # Ensure we always return a tuple

def send_combined_offer(iata_code, city, offers):
    topic_id = ensure_topic_exists(city, iata_code)
    if not topic_id:
        logger.warning(f"⚠️ Kein Topic für {city} ({iata_code})")
        return

    messages = [format_flight_offer(flight) for flight in sorted(offers, key=lambda x: x["type"])]
    full_message = "\n\n".join(messages)

    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
    params = {
        "chat_id": GROUP_ID,
        "text": full_message,
        "message_thread_id": topic_id,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, params=params)
    if response.status_code == 200:
        logger.info(f"✅ Nachricht für {city} ({iata_code}) gesendet.")
    else:
        logger.error(f"❌ Fehler beim Senden an {city} ({iata_code}): {response.text}")

def main():
    logger.info("Starte Abruf von Flugangeboten.")
    offers = fetch_flight_offers()

    if not offers:
        logger.warning("⚠️ Keine Angebote gefunden oder Fehler bei der Abfrage.")
        return

    # Lade gespeicherte Preise aus Gist
    saved_prices = load_file(PRICE_FILENAME)  # Lade die gespeicherten Preise aus Gist
    grouped = defaultdict(list)
    city_map = {}

    for offer in offers:
        iata = offer["iata"]
        city_map[iata] = offer["city"]
        grouped[iata].append(offer)

    for iata_code, flights in grouped.items():
        # Compare each offer with the saved prices
        for flight in flights:
            new_offer, saved_prices = compare_and_update_prices(flight, saved_prices)

            if new_offer:  # Only send the offer if it's new or updated
                send_combined_offer(iata_code, city_map[iata_code], flights)
            else:
                logger.debug(f"Kein neues Angebot für {flight['city']} ({flight['iata']})")

    # Save updated prices to Gist
    save_file("prices.json", saved_prices)  # Save the updated prices in Gist

if __name__ == "__main__":
    main()