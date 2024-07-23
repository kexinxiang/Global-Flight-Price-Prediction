# GCMap Runway Scrape

This folder contains a Python script for scraping the number of runways for various airports from the GCMap website using their IATA codes and updating a MySQL database with this information.

## Files

### `airport_runway_scraper.py`

- **Description:** Scrapes the GCMap website for runway information for airports based on their IATA codes. Updates the MySQL database with the number of runways.
- **Database Dependencies:** Depends on the airport data, including name and IATA code, being preloaded into the Airports table. This allows the script to fetch all airports, send HTTP requests for each, and store the scraped data in the correct database records.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports_with_iata_codes(cursor)`: Fetches a list of airports with valid IATA codes from the database.
  - `update_runway_count(airport_name, runway_count, cursor, connection)`: Updates the runway count for an airport in the database.
  - `scrape_gcmap(airport_name, iata_code)`: Scrapes the GCMap website for the runway count of an airport.
  - `process_airports()`: Main function to process and update runway counts for all airports with valid IATA codes.

## Logging

The script logs its activities to a file named `gcmap_runway_scraper.log`. Check this log for detailed information about the scraping process and any issues encountered.
