import requests
from bs4 import BeautifulSoup
import re
import logging
import random
import time
import mysql.connector

# Configure logging
logging.basicConfig(filename='airport_traffic_scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="flight_database",
        port=3308
    )

def fetch_airports_with_iata_codes(cursor):
    print("Fetching airports with IATA codes")
    cursor.execute("""
        SELECT name, iata_code FROM Airports
        WHERE LENGTH(iata_code) = 3
    """)
    return cursor.fetchall()

def update_airport_info(airport_name, num_destinations, num_airlines, cursor, connection):
    update_query = "UPDATE Airports SET "
    update_values = []
    if num_destinations is not None:
        update_query += "destination_count = %s, "
        update_values.append(num_destinations)
    if num_airlines is not None:
        update_query += "airline_count = %s, "
        update_values.append(num_airlines)

    # Remove trailing comma and add WHERE clause
    update_query = update_query.rstrip(", ") + " WHERE name = %s"
    update_values.append(airport_name)

    cursor.execute(update_query, tuple(update_values))
    connection.commit()

def fetch_traffic_info(airport_name, iata_code):
    url = f"https://www.directflights.com/{iata_code}"  # Replace with the actual URL format
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'},
        {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'},
    ]

    for attempt in range(5):  # Retry logic
        try:
            response = requests.get(url, headers=random.choice(headers), timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            body_text = soup.get_text().lower()

            num_destinations = num_airlines = None

            # Find number of destinations
            destinations_match = re.search(r'with direct flights to (\d+) destinations', body_text)
            if destinations_match:
                num_destinations = int(destinations_match.group(1))

            # Find number of airlines
            airlines_match = re.search(r'there are (\d+) different airlines', body_text)
            if airlines_match:
                num_airlines = int(airlines_match.group(1))

            logging.info(f"{airport_name} ({iata_code}): Destinations: {num_destinations}, Airlines: {num_airlines}")
            return num_destinations, num_airlines

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            time.sleep(random.uniform(1, 5))  # Random wait before retrying

    logging.error(f"Failed to fetch data for {iata_code} after multiple attempts")
    return None, None

def process_airports():
    connection = connect_to_db()
    cursor = connection.cursor()

    airports = fetch_airports_with_iata_codes(cursor)
    total_airports = len(airports)

    print(f"Total airports to process: {total_airports}")

    for index, (airport_name, iata_code) in enumerate(airports, start=1):
        print(f"Processing ({index}/{total_airports}): {airport_name} ({iata_code})")
        num_destinations, num_airlines = fetch_traffic_info(airport_name, iata_code)
        if num_destinations is not None or num_airlines is not None:
            print(f"Updating {airport_name}")
            update_airport_info(airport_name, num_destinations, num_airlines, cursor, connection)

    cursor.close()
    connection.close()

# Process the airports and update the database
process_airports()
