import requests
from bs4 import BeautifulSoup
import mysql.connector
import logging
import re

# Configure logging
logging.basicConfig(filename='gcmap_runway_scraper.log', level=logging.INFO, 
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

def update_runway_count(airport_name, runway_count, cursor, connection):
    update_query = "UPDATE Airports SET runway_count = %s WHERE name = %s"
    cursor.execute(update_query, (runway_count, airport_name))
    connection.commit()

def scrape_gcmap(airport_name, iata_code):
    url = f"http://www.gcmap.com/airport/{iata_code}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; AirportInfoScraper/1.0; +your_email@example.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        runway_count = None

        text = soup.get_text()
        runways_index = text.find("Runways:")
        if runways_index != -1:
            runway_text = text[runways_index:runways_index + 50]  # Get the next 50 characters after "Runways:"
            match = re.search(r'Runways:\s*(\d+)', runway_text)
            if match:
                runway_count = match.group(1)
                logging.info(f"{iata_code}: Runways: {runway_count}")
                return runway_count

        logging.info(f"{airport_name} ({iata_code}): Runways: Not Found")
        return runway_count

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def process_airports():
    connection = connect_to_db()
    cursor = connection.cursor()

    airports = fetch_airports_with_iata_codes(cursor)
    total_airports = len(airports)

    print(f"Total airports to process: {total_airports}")
    
    for index, (airport_name, iata_code) in enumerate(airports, start=1):
        print(f"Processing ({index}/{total_airports}): {airport_name} ({iata_code})")
        runway_count = scrape_gcmap(airport_name, iata_code)
        if runway_count is not None:
            print(f"Updating {airport_name} with Runway Count: {runway_count}")
            update_runway_count(airport_name, runway_count, cursor, connection)

    
    cursor.close()
    connection.close()

# Process the airports and update the database
process_airports()
