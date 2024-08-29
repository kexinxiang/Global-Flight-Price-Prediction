# Route Data Loader

This folder contains a Python script for loading route data from a `.dat` file and storing it either in a MySQL database or as a CSV file, depending on the configuration. The script processes route data, connects to a MySQL database, and handles the storage of route data with reference to airline and airport information.

## Files

### `load-routes.py`

- **Description:** Processes route data from a `.dat` file and stores it into a MySQL database or as a CSV file based on configuration settings. It includes functions to connect to the database, handle CSV and database operations, and manage logging.

- **Database Dependencies:** Requires that the `Airlines` and `Airports` tables are preloaded with the relevant data. The `Routes` table should also be present in the database.

- **Key Functions:**
  - `process_data(filename)`: Reads and parses the `.dat` file, extracting route data.
  - `store_data(data, config)`: Determines the storage method (database or CSV) and invokes the appropriate function.
  - `save_to_database(data, config)`: Connects to the database and inserts route data. Handles logging and error management.
  - `save_as_csv(data, airlines_ref, airports_ref)`: Saves the route data into a CSV file with reference to airline and airport IDs.
  - `load_reference_data()`: Loads airline and airport reference data from CSV files, filtering out airlines without alliances.
  - `connect_to_db(config)`: Establishes a connection to the MySQL database.
  - `get_ids(route, cursor)`: Retrieves IDs for airlines and airports based on route data.

- **Configuration File:**
  - **Path:** `../../configuration/config.json`
  - **Contents:** Specifies the database connection details and the storage method (`database` or `csv`).

- **Logging:**
  - **Log File:** `load-routes.log`
  - **Log Level:** DEBUG
  - **Log Format:** `%(asctime)s - %(levelname)s - %(message)s`

### `Routes.dat`

- **Description:** Input data file in `.dat` format containing route information. The file should be formatted with route details separated by commas.
