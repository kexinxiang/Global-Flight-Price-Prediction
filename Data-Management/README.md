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
  - `configuration/`
  - `data-visualization/`
  - `loading-scripts/` 
  - `scraping-scripts/`

## Description of Folders

### `configuration/`

- **Purpose:** Contains configuration that controls how the data is stored: either in a database or in a `CSV` file.

### `data-visualization/`

- **Purpose:** Stores `CSV` files of Airports, Airlines, Routes, Flights, and Prices data when running scripts of loading data whenc configuration is set to `CSV`.

### `loading-scripts/`

- **Purpose:** Contains scripts for loading `.dat` file directly downloaded from the `openflights.com`. Configuration can be modify to choose the method of storage.

### `scraping-scripts/`

- **Purpose:** Contains scripts for scraping detailed information about airports, airlines, flights, and prices. These scripts update the MySQL database or save as `CSV` in the `data-visualization/` folder with the scraped data.

## Logging

The scripts log their activities to log files within their respective folders. Check these log files for detailed information about the scraping or loading process and any issues encountered.
