# FlightForm Scrape: Airport Destination and Airline Scraper

This folder contains a Python script for scraping traffic information (number of destinations and airlines) for various airports and updating a MySQL database with this information.

## Files

### `airport-dest-airline-scrape.py`

- **Description:** Scrapes traffic information from a flightform's website based on airport IATA codes and updates the MySQL database with the number of destinations and airlines for each airport.
- **Database Dependencies:** Depends on the airport data, including name and IATA code, being preloaded into the `Airports` table. This allows the script to fetch all airports, send HTTP requests for each, and store the scraped data in the correct database records.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports_with_iata_codes(cursor)`: Retrieves a list of airports with valid IATA codes from the database.
  - `update_airport_info(airport_name, num_destinations, num_airlines, cursor, connection)`: Updates the number of destinations and airlines for an airport in the database.
  - `fetch_traffic_info(airport_name, iata_code)`: Scrapes traffic information (number of destinations and airlines) from the website for an airport.
  - `process_airports()`: Main function to process and update traffic information for all airports with valid IATA codes.

## Logging

The script logs its activities to a file named `airport-dest-airline-scrape.log`. Check this log for detailed information about the scraping process, including successes and any issues encountered.
