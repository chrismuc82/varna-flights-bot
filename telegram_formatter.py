from datetime import datetime
from tinyurl_helper import shorten_url  # NEU: TinyURL-Import


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def format_date(date_string):
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return date.strftime("%d. %B %Y")

def format_time(date_string):
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return date.strftime("%H:%M")

def format_flight_offer(flight):
    #short_link = shorten_url(flight['link'])  # Kürze den Link
    short_link = flight['link']

    if flight["type"] == "one-way":
        return (
            f"🛫 {flight['city']}\n"
            f"📅 {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])}\n"
            f"💶 {flight['price']} EUR\n"
            f"⌛ {format_duration(flight['duration'])}\n"
            f"👉 [Zum Angebot]({short_link})"
        )
    else:
        return (
            f"🛫 🔁 🛬 {flight['city']}\n"
            f"📅 {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])} 🛫\n"
            f"⌛️ {format_duration(flight['duration_outbound'])}\n"
            f"📅 {format_date(flight['return_time'])} 🕑 {format_time(flight['return_time'])} 🛬\n"
            f"⌛ {format_duration(flight['duration_inbound'])}\n"
            f"💶 {flight['price']} EUR\n"
            f"👉 [Zum Angebot]({short_link})"
        )
