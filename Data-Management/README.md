# Data Management - Development Cycle 1

This folder contains all the scripts and resources for the first development cycle of the project, focused on loading and scraping data related to airlines and airports and storing them to MySQL database.

## MySQL Database Structure

### `Airports` Table

- `id`: INT, Primary Key
- `name`: VARCHAR(255)
- `iata_code`: VARCHAR(3)
- `city`: VARCHAR(255)
- `country`: VARCHAR(255)
- `latitude`: FLOAT
- `longitude`: FLOAT
- `destination_count`: INT
- `airline_count`: INT
- `annual_passenger`: BIGINT
- `annual_flight`: BIGINT
- `area`: FLOAT
- `gate_count`: INT
- `runway_count`: INT
- `open_date`: DATE

### `Airlines` Table

- `id`: INT, Primary Key
- `name`: VARCHAR(255)
- `iata_code`: VARCHAR(2)
- `icao_code`: VARCHAR(3)
- `country`: VARCHAR(255)
- `fleet_size`: INT
- `destination_count`: INT
- `alliance`: VARCHAR(255)

## Folder Structure

- `data-management/`
  - `airport-info-scraping/`
  - `fleet-dest-scraping/`
  - `load-alliance/`
  - `load-airport-airline-general-info/`

## Description of Folders

### `airport-info-scraping/`

- **Purpose:** Contains scripts for scraping detailed information about airports, such as the number of runways, from various online sources: Wikipedia, FlightForm, and GCmap. These scripts update the MySQL database with the scraped data.

### `fleet-dest-scraping/`

- **Purpose:** Contains scripts for scraping fleet size and destination count information for airlines from Wikipedia. The gathered data is then used to update the relevant fields in the MySQL database.

### `load-alliance/`

- **Purpose:** Includes scripts for loading and updating airline alliance information in the MySQL database. This involves processing text files that list airlines and their corresponding alliances.

### `load-airport-airline-general-info/`

- **Purpose:** Contains scripts for initially loading general information about airports and airlines into the MySQL database from `.dat` files. This includes basic details like names, IATA and ICAO codes, and locations. This serves as the basis information that assits later web scraping scripts.

## Logging

The scripts log their activities to log files within their respective folders. Check these log files for detailed information about the scraping or loading process and any issues encountered.
