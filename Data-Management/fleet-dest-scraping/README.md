# Airline Scraper

This folder contains a Python script for scraping fleet size and destination count information for various airlines from Wikipedia and updating a MySQL database with this information.

## Files

### `airline_scraper.py`

- **Description:** Scrapes Wikipedia for fleet size and destination count information for airlines based on their names. Updates the MySQL database with this information.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airlines(cursor)`: Fetches a list of airlines with valid IATA codes from the database.
  - `update_airline_info(airline_name, fleet_size, destination_count, cursor, connection)`: Updates the fleet size and destination count for an airline in the database.
  - `extract_number(text)`: Extracts the first number found in a given text.
  - `scrape_wikipedia(airline_name)`: Scrapes Wikipedia for fleet size and destination count information of an airline.
  - `process_airlines()`: Main function to process and update fleet size and destination count for all airlines with valid IATA codes.

## Logging

The script logs its activities to a file named `airline_scraper.log`. Check this log for detailed information about the scraping process and any issues encountered.
