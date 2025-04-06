import requests
from telegram_formatter import format_flight_offer
from config import TELEGRAM_API_KEY, GROUP_ID
from topic_manager import ensure_topic_exists
import logging

logger = logging.getLogger(__name__)


def send_flight_offer(flight):
    """Send a flight offer to the corresponding Telegram topic."""
    city = flight["city"]
    iata_code = flight["iata"]
    topic_id = ensure_topic_exists(city, iata_code)

    if topic_id:
        message = format_flight_offer(flight)
        url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
        params = {
            "chat_id": GROUP_ID,
            "text": message,
            "message_thread_id": topic_id,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, params=params)
        if response.status_code == 200:
            logger.info(f"✅ Sent offer to {city} ({iata_code})")
        else:
            logger.error(f"❌ Failed to send message: {response.text}")
    else:
        logger.warning(f"⚠️ No topic for {city} ({iata_code})")


def send_flight_offers(offers):
    """Send all flight offers for a city, ensuring only one push per topic."""
    logger.info("Sending flight offers...")

    # Group offers by topic (city) to avoid sending multiple messages per topic
    grouped_offers = {}
    for flight in offers:
        city = flight["city"]
        if city not in grouped_offers:
            grouped_offers[city] = {"one-way": None, "roundtrip": None}

        if flight["type"] == "one-way":
            grouped_offers[city]["one-way"] = flight
        elif flight["type"] == "roundtrip":
            grouped_offers[city]["roundtrip"] = flight

    # Send each offer group to Telegram
    for city, flights in grouped_offers.items():
        message = ""
        if flights["one-way"]:
            message += format_flight_offer(flights["one-way"])
        if flights["roundtrip"]:
            if message:  # Add separation between one-way and roundtrip if both exist
                message += "\n\n"
            message += format_flight_offer(flights["roundtrip"])

        if message:  # Only send the message if there is content
            topic_id = ensure_topic_exists(city,
                                           flights["one-way"]["iata"] if flights["one-way"] else flights["roundtrip"][
                                               "iata"])
            if topic_id:
                url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
                params = {
                    "chat_id": GROUP_ID,
                    "text": message,
                    "message_thread_id": topic_id,
                    "parse_mode": "Markdown"
                }

                response = requests.post(url, params=params)
                if response.status_code == 200:
                    logger.info(f"✅ Sent offer to {city}")
                else:
                    logger.error(f"❌ Failed to send message for {city}: {response.text}")
            else:
                logger.warning(
                    f"⚠️ No topic for {city} ({flights['one-way']['iata'] if flights['one-way'] else flights['roundtrip']['iata']})")