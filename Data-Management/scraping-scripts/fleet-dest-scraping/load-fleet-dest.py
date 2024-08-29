import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
import logging
import random
import re

# Configure logging
logging.basicConfig(filename='airline_scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="flight_database",
        port = 3308
    )

# Function to fetch airlines from the database
def fetch_airlines(cursor):
    cursor.execute("SELECT name, iata_code FROM Airlines WHERE iata_code IS NOT NULL AND LENGTH(iata_code) < 2")
    print("Fetch all airlines")
    return cursor.fetchall()

# Function to update fleet size and destination count in the database
def update_airline_info(airline_name, fleet_size, destination_count, cursor, connection):
    update_query = """
    UPDATE Airlines
    SET fleet_size = %s, destination_count = %s
    WHERE name = %s
    """
    cursor.execute(update_query, (fleet_size, destination_count, airline_name))
    connection.commit()

def extract_number(text):
    """ Extract the first number found in the text. """
    match = re.search(r'\d+', text)
    if match:
        return int(match.group(0))
    return None

def scrape_wikipedia(airline_name):
    url = f"https://en.wikipedia.org/wiki/{airline_name.replace(' ', '_')}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; AirlineScraper/1.0; +your_email@example.com)'}
    
    for attempt in range(3):  # Retry logic
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            fleet_size = destination_count = None

            # Example of finding fleet size
            try:
                infobox = soup.find('table', {'class': 'infobox'})
                if infobox:
                    rows = infobox.find_all('tr')
                    for row in rows:
                        header = row.find('th')
                        if header and 'Fleet size' in header.text:
                            fleet_size_text = row.find('td').text.strip()
                            # Extract only the numeric part
                            fleet_size = extract_number(fleet_size_text)
                            break
            except Exception as e:
                logging.warning(f"Fleet size parsing error for {airline_name}: {e}")

            # Example of finding destination count
            try:
                infobox = soup.find('table', {'class': 'infobox'})
                if infobox:
                    rows = infobox.find_all('tr')
                    for row in rows:
                        header = row.find('th')
                        if header and 'Destinations' in header.text:
                            destination_count_text = row.find('td').text.strip()
                            # Extract only the numeric part
                            destination_count = extract_number(destination_count_text)
                            break
            except Exception as e:
                logging.warning(f"Destination count parsing error for {airline_name}: {e}")

            return fleet_size, destination_count


        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            #time.sleep(5 + random.uniform(1, 5))  # Random wait before retrying

    logging.error(f"Failed to fetch data for {airline_name} after multiple attempts")
    return None, None

# Function to process airlines and update the database
def process_airlines():
    connection = connect_to_db()
    cursor = connection.cursor()

    airlines = fetch_airlines(cursor)

    for airline_name, iata_code in airlines:
        print("Scraping", airline_name)
        fleet_size, destination_count = scrape_wikipedia(airline_name)
        if fleet_size is not None and destination_count is not None:
            print("updating", airline_name)
            update_airline_info(airline_name, fleet_size, destination_count, cursor, connection)
        #time.sleep(10 + random.uniform(5, 10))  # Random delay between requests

    cursor.close()
    connection.close()

# Process the airlines and update the database
process_airlines()
