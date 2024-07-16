import requests
from bs4 import BeautifulSoup
import re
import logging
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

def fetch_airports_with_null_fields(cursor):
    print("Fetching airports with null annual_passenger or annual_flight")
    cursor.execute("""
        SELECT name FROM Airports
        WHERE (annual_passenger IS NULL OR annual_flight IS NULL) AND open_date IS NULL
    """)
    return cursor.fetchall()

def update_airport_info(airport_name, annual_passenger, annual_flight, cursor, connection):
    update_query = "UPDATE Airports SET "
    update_values = []
    if annual_passenger is not None:
        update_query += "annual_passenger = %s, "
        update_values.append(annual_passenger)
    if annual_flight is not None:
        update_query += "annual_flight = %s, "
        update_values.append(annual_flight)

    # Remove trailing comma and add WHERE clause
    update_query = update_query.rstrip(", ") + " WHERE name = %s"
    update_values.append(airport_name)

    cursor.execute(update_query, tuple(update_values))
    connection.commit()

def extract_number(text):
    """ Extract the first number found in the text, considering possible units like millions or billions. """
    text = text.replace(',', '').lower()
    if 'million' in text:
        match = re.search(r'(\d+(\.\d+)?)', text)
        if match:
            return int(float(match.group(0)) * 1_000_000)
    elif 'billion' in text:
        match = re.search(r'(\d+(\.\d+)?)', text)
        if match:
            return int(float(match.group(0)) * 1_000_000_000)
    else:
        match = re.search(r'\d+', text)
        if match:
            return int(match.group(0))
    return None

def scrape_wikipedia(airport_name):
    url = f"https://en.wikipedia.org/wiki/{airport_name.replace(' ', '_')}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; AirportTrafficScraper/1.0; +your_email@example.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        annual_passenger = annual_flight = None

        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header:
                    header_text = header.text.lower()
                    if 'total passengers' in header_text or 'total number of passengers' in header_text or 'number of passengers' in header_text:
                        passengers_text = row.find('td').text.strip()
                        logging.info(f"Original Passengers Text for {airport_name}: {passengers_text}")
                        annual_passenger = extract_number(passengers_text)
                    elif 'aircraft operations' in header_text or 'aircraft movements' in header_text:
                        flights_text = row.find('td').text.strip()
                        logging.info(f"Original Aircraft Movements Text for {airport_name}: {flights_text}")
                        annual_flight = extract_number(flights_text)

        logging.info(f"{airport_name}: Annual Passengers: {annual_passenger}, Annual Flights: {annual_flight}")
        return annual_passenger, annual_flight

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None, None

def process_airports():
    connection = connect_to_db()
    cursor = connection.cursor()

    airports = fetch_airports_with_null_fields(cursor)
    total_airports = len(airports)

    print(f"Total airports to process: {total_airports}")

    for index, (airport_name,) in enumerate(airports, start=1):
        print(f"Processing ({index}/{total_airports}): {airport_name}")
        annual_passenger, annual_flight = scrape_wikipedia(airport_name)
        if annual_passenger is not None or annual_flight is not None:
            print(f"Updating {airport_name}")
            update_airport_info(airport_name, annual_passenger, annual_flight, cursor, connection)

    cursor.close()
    connection.close()

# Process the airports and update the database
process_airports()
