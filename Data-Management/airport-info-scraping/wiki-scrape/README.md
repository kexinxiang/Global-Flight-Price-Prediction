# Wiki Scrape

This folder contains Python scripts for scraping and updating airport information from Wikipedia. The scripts focus on extracting data such as opened date, runways, passenger statistics, and annual aircraft movements, and then updating a MySQL database with this information.

## Files

### 1. `airport-scrape-wiki.py`

- **Description:** Scrapes Wikipedia for airport information including the opened date, number of runways, annual passenger count, and annual aircraft movements. Updates these details in the MySQL database.
- **Database Dependencies:** Depends on the airport data, including name and IATA code, being preloaded into the Airports table. This allows the script to fetch all airports, send HTTP requests for each, and store the scraped data in the correct database records.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports(cursor)`: Fetches a list of airport names from the database.
  - `update_airport_info()`: Updates the airport information in the database.
  - `extract_number()`: Extracts numerical values from text, handling units like millions and billions.
  - `convert_date()`: Converts various date formats to 'YYYY-MM-DD'.
  - `scrape_wikipedia()`: Scrapes Wikipedia for airport details.
  - `process_airports()`: Main function to process and update airport data.

### 2. `airport-passenger-flight-scrape.py`

- **Description:** Focuses on scraping Wikipedia for annual passenger and aircraft movement statistics for airports. Updates the database with this information if not already present. 
- **Database Dependencies:** Depends on the airport general information, such as name and IATA code, being loaded already, so that we can fetch all airports and send HTTP requests using airport names, and store scraped data to the correct line.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports_with_null_fields(cursor)`: Fetches airports with missing annual passenger or flight data.
  - `update_airport_info()`: Updates airport statistics in the database.
  - `extract_number()`: Extracts numerical values from text.
  - `scrape_wikipedia()`: Scrapes Wikipedia for passenger and aircraft movement statistics.
  - `process_airports()`: Main function to process and update airport statistics.

## Logging

Both scripts log their activities to files (`airport_scraper.log` and `airport_traffic_scraper.log`). Check these logs for detailed information about the scraping process and any issues encountered.

