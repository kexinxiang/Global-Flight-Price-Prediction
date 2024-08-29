import mysql.connector
import csv
import os
import json
import logging

# Configure logging
logging.basicConfig(
    filename='load-routes.log',  # Log file name
    level=logging.DEBUG,       # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
)

#Function that process .dat file
def process_data(filename):
    data_to_insert = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Example: Assuming .dat file format is comma-separated
            fields = line.strip().split(',')
            if len(fields) >= 6:  # Ensure at least 7 fields are present
                airline = fields[0].strip('"')
                origin_airport = fields[2].strip('"')
                dest_airport = fields[4].strip('"')

                data_to_insert.append((airline, origin_airport, dest_airport))

    return data_to_insert


#Function that process config to determine storing method
def store_data(data, config):
    if config["storage_method"] == "database":
        save_to_database(data, config)
    elif config["storage_method"] == "csv":
        airlines_ref, airports_ref = load_reference_data()
        save_as_csv(data, airlines_ref, airports_ref)
    else:
        print("Invalid Storage Method")

#Function that stores data to database
def save_to_database(data, config):
    logging.info("Saving data to the database")
    try:
        connection = connect_to_db(config)
        cursor = connection.cursor()

        for route in data:
            airline_id, origin_airport_id, dest_airport_id = get_ids(route, cursor)
            if airline_id is not None and origin_airport_id is not None and dest_airport_id is not None:
                cursor.execute("""
                    INSERT INTO Routes (airline_code, airline_id, origin_airport_code, origin_airport_id, 
                                        dest_airport_code, dest_airport_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (route[0], airline_id, route[1], origin_airport_id, route[2], dest_airport_id))
                connection.commit()
                logging.debug(f"Inserted route: {route}")
        cursor.close()
        connection.close()
        logging.info("Data successfully saved to the database")
    except mysql.connector.Error as err:
        logging.error(f"Database Error: {err}")
    except Exception as e:
        logging.error(f"Error saving data to the database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to load the reference data from CSV files
def load_reference_data():
    airlines = {}
    airports = {}

    with open('../../data-visualization/Airlines.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['alliance'] != "NULL":
                airlines[row['iata_code']] = row['id']

    with open('../../data-visualization/Airports.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports[row['iata_code']] = row['id']

    return airlines, airports

def save_as_csv(data, airlines_ref, airports_ref):
    logging.info("Saving data as csv")
    with open('../../data-visualization/Routes.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'airline_code', 'airline_id', 'origin_airport_code', 'origin_airport_id', 'dest_airport_code', 'dest_airport_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        i = 1 #initialize idx

        for idx, route in enumerate(data, start=1):
            
            airline_id = airlines_ref.get(route[0])
            origin_airport_id = airports_ref.get(route[1])
            dest_airport_id = airports_ref.get(route[2])

            if airline_id and origin_airport_id and dest_airport_id:
                writer.writerow({
                    'id': i,
                    'airline_code': route[0],
                    'airline_id': airline_id,
                    'origin_airport_code': route[1],
                    'origin_airport_id': origin_airport_id,
                    'dest_airport_code': route[2],
                    'dest_airport_id': dest_airport_id
                })
                i += 1 #increment idx
            

#Function to connect to database
def connect_to_db(config):
     return mysql.connector.connect(
        host = config["db_host"],
        user = config["db_user"],
        password = config["db_password"],
        database = config["db_name"],
        port = config["db_port"],
        buffered = True  # This fetches all results, avoiding the unread results error
    )

# Function to get IDs from the database
def get_ids(route, cursor):
    cursor.execute("SELECT id FROM Airlines WHERE iata_code = %s AND alliance IS NOT NULL", (route[0],))
    airline = cursor.fetchone()

    cursor.execute("SELECT id FROM Airports WHERE iata_code = %s", (route[1],))
    origin_airport = cursor.fetchone()

    cursor.execute("SELECT id FROM Airports WHERE iata_code = %s", (route[2],))
    dest_airport = cursor.fetchone()

    if airline and origin_airport and dest_airport:
        return airline[0], origin_airport[0], dest_airport[0]
    return None, None, None

# Main script starts here
with open('../../configuration/config.json', 'r') as f:
    config = json.load(f)

routes_data = process_data("Routes.dat")
store_data(routes_data, config)
