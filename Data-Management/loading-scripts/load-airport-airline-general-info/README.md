# Airline and Airport Data Importer

This folder contains Python scripts for importing airline and airport data from `.dat` files into a MySQL database and updating ICAO codes for airlines.

## Files

### `import-airline.py`

- **Description:** Processes `airline.dat` containing airline information and inserts the data into a MySQL database.
- **Key Functions:**
  - `process_dat_file(filename)`: Reads and processes the `airlines.dat` file, extracting relevant fields.
  - Inserts airline data into the MySQL `Airlines` table.

### `import-airport.py`

- **Description:** Processes `airport.dat` containing airport information and inserts the data into a MySQL database.
- **Key Functions:**
  - `process_dat_file(filename)`: Reads and processes the `airports.dat` file, extracting relevant fields and validating latitude and longitude.
  - Inserts airport data into the MySQL `Airports` table.

### `load-icao-code.py`

- **Description:** Updates the ICAO codes for airlines in the MySQL database using data from `airlines.dat` file. Previously not loaded but found scraping could be easier if having ICAO code, therefore added this additional file that loads ICAO code for each airline.
- **Key Functions:**
  - `process_dat_file(filename, cursor, conn)`: Reads and processes the airline `.dat` file, extracting ICAO codes and updating the MySQL `Airlines` table.
