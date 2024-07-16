import requests
from bs4 import BeautifulSoup
import re
import logging
import time
import random
from datetime import datetime
import mysql.connector

# Configure logging
logging.basicConfig(filename='airport_scraper.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="flight_database",
        port=3308
    )

def fetch_airports(cursor):
    print("Fetch all airport")
    cursor.execute("SELECT name FROM Airports")
    return cursor.fetchall()

def update_airport_info(airport_name, opened_date, runways, passengers, aircraft_movements, cursor, connection):
    update_query = "UPDATE Airports SET "
    update_values = []
    if opened_date is not None:
        update_query += "open_date = %s, "
        update_values.append(opened_date)
    if runways is not None:
        update_query += "runway_count = %s, "
        update_values.append(runways)
    if passengers is not None:
        update_query += "annual_passenger = %s, "
        update_values.append(passengers)
    if aircraft_movements is not None:
        update_query += "annual_flight = %s, "
        update_values.append(aircraft_movements)

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

def convert_date(date_str):
    """ Convert date from 'day month, year' or 'Month day, year' format to 'YYYY-MM-DD' format. """
    # Check for date within parentheses first
    date_in_parentheses = re.search(r'\((\d{4}-\d{2}-\d{2})\)', date_str)
    if date_in_parentheses:
        return date_in_parentheses.group(1)

    # Extract the primary date part from the string using regex
    date_match = re.search(r'(\d{1,2} \w+ \d{4}|\w+ \d{1,2}, \d{4})', date_str)
    if date_match:
        date_str = date_match.group(0)
    else:
        # Fallback to extracting only the year if no full date is found
        year_match = re.search(r'(\d{4})', date_str)
        if year_match:
            return f"{year_match.group(0)}-01-01"  # Default to January 1st if only the year is available
        return None

    try:
        return datetime.strptime(date_str, '%d %B %Y').strftime('%Y-%m-%d')
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, '%B %Y').strftime('%Y-%m-%d')
    except ValueError:
        pass

    return None


def scrape_wikipedia(airport_name):
    url = f"https://en.wikipedia.org/wiki/{airport_name.replace(' ', '_')}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; AirportScraper/1.0; +your_email@example.com)'}
    
    for attempt in range(3):  # Retry logic
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            opened_date = runways = passengers = aircraft_movements = None

            try:
                infobox = soup.find('table', {'class': 'infobox'})
                if infobox:
                    rows = infobox.find_all('tr')
                    for row in rows:
                        header = row.find('th')
                        if header and 'Opened' in header.text:
                            opened_date_text = row.find('td').text.strip()
                            logging.info(f"Original Opened Date Text for {airport_name}: {opened_date_text}")
                            opened_date = convert_date(opened_date_text.split('\n')[0].strip())
                            break
            except Exception as e:
                logging.warning(f"Opened date parsing error for {airport_name}: {e}")

            try:
                if infobox:
                    infobox_text = infobox.get_text().lower()
                    runways = infobox_text.count('asphalt') + infobox_text.count('concrete')
            except Exception as e:
                logging.warning(f"Runways parsing error for {airport_name}: {e}")

            try:
                if infobox:
                    for row in rows:
                        header = row.find('th')
                        if header and 'Passengers' in header.text:
                            passengers_text = row.find('td').text.strip()
                            passengers_text = passengers_text.split(' ')[0]  # Take only the first segment
                            logging.info(f"Original Passengers Text for {airport_name}: {passengers_text}")
                            passengers = extract_number(passengers_text)
                            break
            except Exception as e:
                logging.warning(f"Passengers parsing error for {airport_name}: {e}")

            try:
                if infobox:
                    for row in rows:
                        header = row.find('th')
                        if header and 'Aircraft movements' in header.text:
                            aircraft_movements_text = row.find('td').text.strip()
                            logging.info(f"Original Aircraft Movements Text for {airport_name}: {aircraft_movements_text}")
                            aircraft_movements = extract_number(aircraft_movements_text)
                            break
            except Exception as e:
                logging.warning(f"Aircraft movements parsing error for {airport_name}: {e}")

            logging.info(f"{airport_name}: Opened Date: {opened_date}, Runways: {runways}, Passengers: {passengers}, Aircraft Movements: {aircraft_movements}")

            return opened_date, runways, passengers, aircraft_movements

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            #time.sleep(5 + random.uniform(1, 5))  # Random wait before retrying

    logging.error(f"Failed to fetch data for {airport_name} after multiple attempts")
    return None, None, None, None

def process_airports():
    connection = connect_to_db()
    cursor = connection.cursor()

    airports = fetch_airports(cursor)

    for airport_name, in airports:
        print("Scraping", airport_name)
        opened_date, runways, passengers, aircraft_movements = scrape_wikipedia(airport_name)
        if opened_date is not None or runways is not None or passengers is not None or aircraft_movements is not None:
            print("Updating", airport_name)
            update_airport_info(airport_name, opened_date, runways, passengers, aircraft_movements, cursor, connection)

    cursor.close()
    connection.close()

# Process the airports and update the database
process_airports()
