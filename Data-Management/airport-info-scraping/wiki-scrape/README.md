# Wiki Scrape

This folder contains Python scripts for scraping and updating airport information from Wikipedia. The scripts focus on extracting data such as opened date, runways, passenger statistics, and annual aircraft movements, and then updating a MySQL database with this information.

## Files

### 1. `airport_scraper.py`

- **Description:** Scrapes Wikipedia for airport information including the opened date, number of runways, annual passenger count, and annual aircraft movements. Updates these details in the MySQL database.
- **Database Dependencies:** Depends on the airport general information, such as name and IATA code, being loaded already, so that we can fetch all airports and send HTTP requests using airport names, and store scraped data to the correct line.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports(cursor)`: Fetches a list of airport names from the database.
  - `update_airport_info()`: Updates the airport information in the database.
  - `extract_number()`: Extracts numerical values from text, handling units like millions and billions.
  - `convert_date()`: Converts various date formats to 'YYYY-MM-DD'.
  - `scrape_wikipedia()`: Scrapes Wikipedia for airport details.
  - `process_airports()`: Main function to process and update airport data.

### 2. `airport_traffic_scraper.py`

- **Description:** Focuses on scraping Wikipedia for annual passenger and aircraft movement statistics for airports. Updates the database with this information if not already present.
- **Database Dependencies:** Depends on the airport general information, such as name and IATA code, being loaded already, so that we can fetch all airports and send HTTP requests using airport names, and store scraped data to the correct line.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `fetch_airports_with_null_fields(cursor)`: Fetches airports with missing annual passenger or flight data.
  - `update_airport_info()`: Updates airport statistics in the database.
  - `extract_number()`: Extracts numerical values from text.
  - `scrape_wikipedia()`: Scrapes Wikipedia for passenger and aircraft movement statistics.
  - `process_airports()`: Main function to process and update airport statistics.

## Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    ```
2. **Navigate to the `wiki-scrape` Folder:**
    ```bash
    cd yourproject/wiki-scrape
    ```
3. **Install Dependencies:**
    Ensure you have the required libraries installed. You can install them using pip:
    ```bash
    pip install requests beautifulsoup4 mysql-connector-python
    ```

## Configuration

- **Database Configuration:**
  Edit the `connect_to_db()` function in both scripts to match your database credentials and connection details.

## Usage

1. **Run `airport_scraper.py`:**
    ```bash
    python airport_scraper.py
    ```
   This script will scrape and update general airport information.

2. **Run `airport_traffic_scraper.py`:**
    ```bash
    python airport_traffic_scraper.py
    ```
   This script will scrape and update annual passenger and flight statistics.

## Logging

Both scripts log their activities to files (`airport_scraper.log` and `airport_traffic_scraper.log`). Check these logs for detailed information about the scraping process and any issues encountered.

## Contact

For any questions or feedback, please contact [your.email@example.com](mailto:your.email@example.com).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

