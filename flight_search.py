import requests
import datetime
from config import KIWI_API_KEY

def fetch_flight_offers():
    url = "https://api.tequila.kiwi.com/v2/search"
    headers = {"accept": "application/json", "apikey": KIWI_API_KEY}

    today = datetime.datetime.today().strftime("%d/%m/%Y")
    three_months_later = (datetime.datetime.today() + datetime.timedelta(days=90)).strftime("%d/%m/%Y")
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
    one_way_response = requests.get(url, headers=headers, params=common_params)
    # Roundtrip flights
    roundtrip_params = common_params.copy()
    roundtrip_params.update({
        "return_from": today,
        "return_to": two_weeks_later,
    })
    roundtrip_response = requests.get(url, headers=headers, params=roundtrip_params)

    flight_data = {}

    # Process One-Way Flights
    if one_way_response.status_code == 200:
        for flight in one_way_response.json().get("data", []):
            iata = flight["cityCodeTo"]
            if iata not in flight_data or flight["price"] < flight_data[iata]["price"]:
                flight_data[iata] = {
                    "city": flight["cityTo"],
                    "iata": iata,
                    "price": flight["price"],
                    "departure_time": flight["local_departure"],
                    "return_time": None,
                    "duration": flight["duration"]["departure"],
                    "link": flight["deep_link"],
                    "type": "one-way"
                }

    # Process Roundtrip Flights
    if roundtrip_response.status_code == 200:
        for flight in roundtrip_response.json().get("data", []):
            iata = flight["cityCodeTo"]
            if iata not in flight_data or flight["price"] < flight_data[iata]["price"]:
                flight_data[iata] = {
                    "city": flight["cityTo"],
                    "iata": iata,
                    "price": flight["price"],
                    "departure_time": flight["local_departure"],
                    "return_time": flight["route"][-1]["local_departure"],
                    "duration_outbound": flight["duration"]["departure"],
                    "duration_inbound": flight["duration"]["return"],
                    "link": flight["deep_link"],
                    "type": "roundtrip"
                }

    return list(flight_data.values())
