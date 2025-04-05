from datetime import datetime
import locale

# Stelle sicher, dass Deutsch verwendet wird
try:
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "de_DE")  # Fallback für Windows/Linux

def format_date(date_str):
    """Format ISO datetime string to '15. April 2024'."""
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z")
    return dt.strftime("%-d. %B %Y")  # z.B. '15. April 2024'

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    date_formatted = dt.strftime("%d. %B %Y")
    time_formatted = dt.strftime("%H:%M")
    return date_formatted, time_formatted

def format_flight_offer(flight):
    if flight["type"] == "one-way":
        duration_minutes = flight["duration"] // 60
        message = (
            f"🛫 {flight['city']} ({flight['iata']})\n"
            f"📅 {format_date(flight['departure_time'])}\n"
            f"⏱️ Flugdauer: {duration_minutes} Min\n"
            f"💶 Preis: {flight['price']} EUR\n"
            f"🔗 [Zur Buchung]({flight['link']})"
        )
    elif flight["type"] == "roundtrip":
        outbound_minutes = flight["duration_outbound"] // 60
        inbound_minutes = flight["duration_inbound"] // 60
        message = (
            f"🛫 {flight['city']} ({flight['iata']})\n"
            f"📅 Hinflug: {format_date(flight['departure_time'])} ({outbound_minutes} Min)\n"
            f"📅 Rückflug: {format_date(flight['return_time'])} ({inbound_minutes} Min)\n"
            f"💶 Preis: {flight['price']} EUR\n"
            f"🔗 [Zur Buchung]({flight['link']})"
        )
    else:
        message = "❌ Unbekannter Flugtyp"

    return message
