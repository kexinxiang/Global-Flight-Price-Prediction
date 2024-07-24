import mysql.connector

def process_dat_file(filename, cursor, conn):
    data_to_insert = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Example: Assuming .dat file format is comma-separated
            fields = line.strip().split(',')
            if len(fields) >= 7:  # Ensure at least 7 fields are present
                name =  fields[1].strip('"')
                icao_code = fields[4].strip('"')

                if icao_code not in ["\\N", "N/A"]:
                        # Insert data into MySQL table
                    update_query = "UPDATE Airlines SET icao_code = %s WHERE name = %s"
                    cursor.execute(update_query, (icao_code, name))
                    conn.commit()

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


print("Start Inserting")
process_dat_file(filename, cursor, conn)

# Close connection
cursor.close()
conn.close()

print("Data inserted successfully into MySQL.")