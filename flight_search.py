import requests
import datetime
import time
import logging
from config import KIWI_API_KEY
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


def add_timestamp(offer):
    """Add a timestamp to the offer when it's first saved."""
    offer["timestamp"] = time.time()  # Get the current time in seconds since epoch
    return offer


def extract_flights_id(deep_link):
    """Extract flightsId from the deep_link URL."""
    try:
        parsed_url = urlparse(deep_link)
        query_params = parse_qs(parsed_url.query)
        flights_id = query_params.get('flightsId', [None])[0]
        if flights_id:
            return flights_id
        else:
            logger.warning("Keine flightsId im Deeplink gefunden.")
            return None
    except Exception as e:
        logger.error("Fehler beim Extrahieren der flightsId aus dem Deeplink: %s", e)
        return None


def fetch_flight_offers():
    logger.info("Starte Abruf von Flugangeboten...")

    url = "https://api.tequila.kiwi.com/v2/search"
    headers = {"accept": "application/json", "apikey": KIWI_API_KEY}

    today = datetime.datetime.today().strftime("%d/%m/%Y")

    ''' three_months_later = (datetime.datetime.today() + datetime.timedelta(days=90)).strftime("%d/%m/%Y")
        one_month_later = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime("%d/%m/%Y") 
        two_weeks_later = (datetime.datetime.today() + datetime.timedelta(days=14)).strftime("%d/%m/%Y")
    '''
    two_month_later = (datetime.datetime.today() + datetime.timedelta(days=60)).strftime("%d/%m/%Y")
    three_months_later = (datetime.datetime.today() + datetime.timedelta(days=90)).strftime("%d/%m/%Y")

    common_params = {
        "fly_from": "VAR",
        "fly_to": "DE",
        "date_from": today,
        "date_to": three_months_later,
        "curr": "EUR",
        "limit": 500,
        "sort": "price",
        "asc": 1,
        "locale": "de"
    }

    one_way_flights = {}
    roundtrip_flights = {}

    # One-way
    one_way_params = {**common_params, "return_from": "", "return_to": ""}
    one_way_response = requests.get(url, headers=headers, params=one_way_params)

    if one_way_response.status_code == 200:
        data = one_way_response.json().get("data", [])
        logger.info("One-Way-Flüge erfolgreich abgerufen: %d Angebote", len(data))

        for flight in data:
            iata = flight["cityCodeTo"]
            flight_id = extract_flights_id(flight["deep_link"])  # Extract 'flightsId' from 'link' field
            if iata not in one_way_flights or flight["price"] < one_way_flights[iata]["price"]:
                one_way_flights[iata] = add_timestamp({
                    "city": flight["cityTo"],
                    "iata": iata,
                    "price": flight["price"],
                    "departure_time": flight["local_departure"],
                    "return_time": None,
                    "duration": flight["duration"]["departure"],
                    "link": flight["deep_link"],
                    "flightsId": flight_id,  # Save the flightsId
                    "type": "one-way"
                })
    else:
        logger.error("Fehler beim Abrufen der One-Way-Flüge: %s", one_way_response.text)

    '''
    # Roundtrip Flights
    #roundtrip_params = {**common_params, "return_from": two_weeks_later, "return_to": one_month_later}
    '''
    roundtrip_params = {**common_params, "nights_in_dst_from": 3, "nights_in_dst_to": 14}
    roundtrip_response = requests.get(url, headers=headers, params=roundtrip_params)

    if roundtrip_response.status_code == 200:
        data = roundtrip_response.json().get("data", [])
        logger.info("Roundtrip-Flüge erfolgreich abgerufen: %d Angebote", len(data))

        skipped = 0

        for flight in data:
            outbound_dest = flight["route"][0]["flyTo"]
            inbound_origin = flight["route"][-1]["flyFrom"]

            # Filter für unpassende Flughäfen
            if outbound_dest != inbound_origin:
                logger.debug(  # NEU
                    "Überspringe Roundtrip: Hinflug endet in %s, Rückflug startet in %s",  # NEU
                    outbound_dest, inbound_origin  # NEU
                )  # NEU
                skipped += 1  # NEU
                continue  # NEU

            iata = flight["cityCodeTo"]
            flight_id = extract_flights_id(flight["deep_link"])  # Extract 'flightsId' from 'link' field
            if iata not in roundtrip_flights or flight["price"] < roundtrip_flights[iata]["price"]:
                roundtrip_flights[iata] = add_timestamp({
                    "city": flight["cityTo"],
                    "iata": iata,
                    "price": flight["price"],
                    "departure_time": flight["local_departure"],
                    "return_time": flight["route"][-1]["local_departure"],
                    "duration_outbound": flight["duration"]["departure"],
                    "duration_inbound": flight["duration"]["return"],
                    "link": flight["deep_link"],
                    "flightsId": flight_id,  # Save the flightsId
                    "type": "roundtrip"
                })
        logger.info("Übersprungene Roundtrips wegen unterschiedlicher Flughäfen: %d", skipped)  # NEU

    else:
        logger.error("Fehler beim Abrufen der Roundtrip-Flüge: %s", roundtrip_response.text)

    all_flights = list(one_way_flights.values()) + list(roundtrip_flights.values())

    if not all_flights:
        logger.warning("Keine Flugangebote gefunden.")
    else:
        logger.info("Insgesamt %d Angebote (One-Way + Roundtrip) ausgewählt.", len(all_flights))

    return all_flights
