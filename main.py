import requests
from flight_search import fetch_flight_offers
from topic_manager import ensure_topic_exists
from config import TELEGRAM_API_KEY, GROUP_ID
from telegram_formatter import format_flight_offer


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
            print(f"✅ Sent offer to {city} ({iata_code})")
        else:
            print(f"❌ Failed to send message: {response.text}")
    else:
        print(f"⚠️ No topic for {city} ({iata_code})")


def main():
    offers = fetch_flight_offers()
    for flight in offers:
        send_flight_offer(flight)


if __name__ == "__main__":
    main()
