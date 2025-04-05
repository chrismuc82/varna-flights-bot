from datetime import datetime

def format_duration(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if hours else f"{mins}m"

def format_date(date_string):
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return date.strftime("%d. %B %Y")

def format_time(date_string):
    date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return date.strftime("%H:%M")

def format_flight_offer(flight):
    if flight["type"] == "one-way":
        return (
            f"🛫 {flight['city']} ({flight['iata']})\n"
            f"📅 {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])}\n"
            f"🛫️ Flugzeit: {format_duration(flight['duration'])}\n"
            f"💶 {flight['price']} EUR\n"
            f"👉 [Jetzt buchen]({flight['link']})"
        )
    else:
        return (
            f"🛫 🔁 🛬 {flight['city']} ({flight['iata']})\n"
            f"📅 Hinflug: {format_date(flight['departure_time'])} 🕑 {format_time(flight['departure_time'])}\n"
            f"   🛫️ {format_duration(flight['duration_outbound'])}\n"
            f"📅 Rückflug: {format_date(flight['return_time'])} 🕑 {format_time(flight['return_time'])}\n"
            f"   🛫 {format_duration(flight['duration_inbound'])}\n"
            f"💶 {flight['price']} EUR\n"
            f"👉 [Jetzt buchen]({flight['link']})"
        )
