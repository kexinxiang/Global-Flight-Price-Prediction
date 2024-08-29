# Loading Scripts

This folders contains scripst that load data from `.dat` file to the MySQL database or save as `CSV` file in the `data-visualization/` directory.

## Folder Structures

### `load-alliance/`

- **Purpose:** Includes scripts for loading and updating airline alliance information in the MySQL database. This involves processing text files that list airlines and their corresponding alliances.

### `load-airport-airline-general-info/`

- **Purpose:** Contains scripts for initially loading general information about airports and airlines into the MySQL database from `.dat` files. This includes basic details like names, IATA and ICAO codes, and locations. This serves as the basis information that assits later web scraping scripts.

### `load-routes/`

- **Purpose:** Contains scripts for initially loading routes information into the MySQL database or saving as `CSV` from `.dat` files. This includes basic details like airline codes, origin airport and destination airport codes. This serves as the basis information that assits later web scraping scripts for flight information.