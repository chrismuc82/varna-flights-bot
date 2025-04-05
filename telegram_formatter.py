from datetime import datetime

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    date_formatted = dt.strftime("%d. %B %Y")
    time_formatted = dt.strftime("%H:%M")
    return date_formatted, time_formatted

def format_flight_offer(flight):
    price = flight["price"]

    # One-way flight
    if flight["type"] == "one-way":
        departure_date, departure_time = format_datetime(flight["departure_time"])
        duration_minutes = flight["duration_outbound"] // 60
        duration_str = f"{duration_minutes // 60}h {duration_minutes % 60}m"

        message = (
            f"📅 {departure_date} | 💶 {price}€ | 🛫 Einfachflug\n"
            f"⏳ Dauer: {duration_str} | Abflug: {departure_time} Uhr"
        )

    # Roundtrip flight
    else:
        outbound_date, outbound_time = format_datetime(flight["departure_time"])
        return_date, return_time = format_datetime(flight["return_time"])

        outbound_duration = flight["duration_outbound"] // 60
        inbound_duration = flight["duration_inbound"] // 60

        outbound_duration_str = f"{outbound_duration // 60}h {outbound_duration % 60}m"
        inbound_duration_str = f"{inbound_duration // 60}h {inbound_duration % 60}m"

        message = (
            f"📅 {outbound_date} - {return_date} | 💶 {price}€ | 🔄 Hin- & Rückflug\n"
            f"🛫 Hinflug: {outbound_time} Uhr ({outbound_duration_str})\n"
            f"🛬 Rückflug: {return_time} Uhr ({inbound_duration_str})"
        )

    return message
