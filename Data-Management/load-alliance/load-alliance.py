import mysql.connector

# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="flight_database",
        port = 3308
    )

# Function to update the alliance information in the database
def update_alliance(airline_iata, alliance, cursor, connection):
    update_query = """
    UPDATE Airlines
    SET alliance = %s
    WHERE iata_code = %s
    """
    cursor.execute(update_query, (alliance, airline_iata))
    connection.commit()

# Function to process the files and update the database
def process_alliance_files(file_paths):
    connection = connect_to_db()
    cursor = connection.cursor()

    for file_path, alliance in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                name, iata_code = line.strip().split(', ')
                if iata_code:  # Only process if IATA code is not null
                    print("Start processing", alliance)
                    update_alliance(iata_code, alliance, cursor, connection)

    print("All Done")

    cursor.close()
    connection.close()

# List of file paths and their corresponding alliances
alliance_files = [
    ('StarAlliance.txt', 'Star Alliance'),
    ('OneWorld.txt', 'Oneworld'),
    ('SkyTeam.txt', 'SkyTeam'),
    ('U-FlYAlliance.txt', 'U-FLY Alliance'),
    ('ValueAlliance.txt', 'Value Alliance'),
    ('VanillaAlliance.txt', 'Vanilla Alliance'),
]

# Process the files and update the database
process_alliance_files(alliance_files)
