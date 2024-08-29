# Airline Alliance Updater

This folder contains a Python script for updating airline alliance information in a MySQL database based on data from text files storing airlines for each alliance.

## Files

### `load-alliance.py`

- **Description:** Reads alliance information from text files and updates the MySQL database with this information.
- **Database Dependencies:** Depends on the airline data, including name and IATA code, being preloaded into the `Airlines` table. This allows the script to store the scraped data in the correct database records.
- **Key Functions:**
  - `connect_to_db()`: Connects to the MySQL database.
  - `update_alliance(airline_iata, alliance, cursor, connection)`: Updates the alliance information for an airline in the database.
  - `process_alliance_files(file_paths)`: Processes the files containing alliance information and updates the database.
