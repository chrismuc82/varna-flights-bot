import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def format_date(date_string):
    try:
        date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return date.strftime("%d. %B %Y")
    except Exception as e:
        logger.error("Error formatting date: %s (%s)", date_string, e, exc_info=True)
        return "?"

def format_time(date_string):
    try:
        date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return date.strftime("%H:%M")
    except Exception as e:
        logger.error("Error formatting time: %s (%s)", date_string, e, exc_info=True)
        return "?"

def format_flight_offer(flight):
    try:
        if flight["type"] == "one-way":
            return (
                f"🛫 {flight['city']} ({flight['iata']})\n"
                f"📅 {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])}\n"
                f"✈️ Flugzeit: {format_duration(flight['duration'])}\n"
                f"💶 {flight['price']} EUR\n"
                f"👉 [Jetzt buchen]({flight['link']})"
            )
        else:
            return (
                f"🛫 🔁 {flight['city']} ({flight['iata']})\n"
                f"📅 Hinflug: {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])}\n"
                f"   ✈️ {format_duration(flight['duration_outbound'])}\n"
                f"📅 Rückflug: {format_date(flight['return_time'])} 🕑 {format_time(flight['return_time'])}\n"
                f"   ✈️ {format_duration(flight['duration_inbound'])}\n"
                f"💶 {flight['price']} EUR\n"
                f"👉 [Jetzt buchen]({flight['link']})"
            )
    except Exception as e:
        logger.error("Error formatting flight offer: %s", flight, exc_info=True)
        return "❌ Fehler bei der Angebotsdarstellung"