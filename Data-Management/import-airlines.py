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
                iata_code = fields[3].strip('"')
                country = fields[6].strip('"')

                data_to_insert.append((name, iata_code,country))

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
filename = 'airlines.dat'
data_to_insert = process_dat_file(filename)

print("Start Inserting")

# Insert data into MySQL table
insert_query = "INSERT INTO Airlines (`name`, `iata_code`, `country`) VALUES (%s, %s, %s)"
cursor.executemany(insert_query, data_to_insert)
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Data inserted successfully into MySQL.")