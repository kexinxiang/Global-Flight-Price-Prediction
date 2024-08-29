# Airport Information Scraping

This folder contains Python scripts for scraping various types of airport information from different sources and updating a MySQL database with the gathered data. The information scraped includes runway counts, open date, and additional details like passenger numbers and aircraft movements.

## Folders and Scripts

### FlightForm Scrape: Airport Destination and Airline Scraper

**Folder**: `flightform-scrape`

This folder contains a Python script for scraping traffic information (number of destinations and airlines) from FlightForm’s website based on airport IATA codes. The script updates the MySQL database with the number of destinations and airlines for each airport.

### GCMap Runway Scrape

**Folder**: `gcmap-runway-scrape`

This folder contains a Python script for scraping runway information from the GCMap website using airport IATA codes and updating the MySQL database.

### Wiki Scrape

**Folder**: `wiki-scrape`

This folder contains Python scripts for scraping and updating various airport details from Wikipedia. This includes information such as the airport’s opening date, runways, passenger statistics, and annual aircraft movements.

