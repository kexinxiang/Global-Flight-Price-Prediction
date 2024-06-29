import mysql.connector
import logging

def process_dat_file(filename):
    data_to_insert = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Example: Assuming .dat file format is comma-separated
            fields = line.strip().split(',')
            if len(fields) >= 7:  # Ensure at least 7 fields are present
                id = fields[0].strip('"')
                name = fields[1].strip('"')
                city = fields[2].strip('"')
                country = fields[3].strip('"')
                iata_code = fields[4].strip('"')
                latitude = fields[6].strip('"')
                longitude = fields[7].strip('"')

                # Validate latitude and longitude
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)
                    # Example: Create a tuple with the data
                    data_to_insert.append((name, iata_code, city, country, latitude, longitude))
                except ValueError:
                    logging.warning(f"Invalid data at line {line_number}: {line.strip()}")
                    continue

    return data_to_insert

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="flight_database",
    port = 3308
)
cursor = conn.cursor()

# Process .dat file
filename = 'airports.dat'
data_to_insert = process_dat_file(filename)

print("Start Inserting")

# Insert data into MySQL table
insert_query = "INSERT INTO Airports (`name`, `iata_code`, `city`, `country`, `latitude`, `longitude`) VALUES (%s, %s, %s, %s, %s, %s)"
cursor.executemany(insert_query, data_to_insert)
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Data inserted successfully into MySQL.")