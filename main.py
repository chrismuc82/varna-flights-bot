from flight_search import fetch_flight_offers
from telegram_formatter import format_flight_offer
from telegram_sender import send_message_to_topic
from topic_manager import ensure_topic_exists

def main():
    flights = fetch_flight_offers()
    for flight in flights:
        print(flight)
        message = format_flight_offer(flight)
        topic_id = ensure_topic_exists(flight["city"], flight["iata"])
        send_message_to_topic(topic_id, message)

if __name__ == "__main__":
    main()
