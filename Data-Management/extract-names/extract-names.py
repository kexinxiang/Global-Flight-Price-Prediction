import mysql.connector

# Step 1: Connect to the MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database="flight_database",
    port = 3308
)

cursor = conn.cursor()

# Step 2: Execute the SQL query to fetch the specific column
query = "SELECT name FROM Airlines"
cursor.execute(query)

# Step 3: Fetch all rows from the executed query
rows = cursor.fetchall()

# Step 4: Write the results to a text file
with open('airline-names.txt', 'w') as file:
    for row in rows:
        file.write(str(row[0]) + '\n')

query = "SELECT name FROM Airports"
cursor.execute(query)

rows = cursor.fetchall()

# Step 4: Write the results to a text file
with open('airport-names.txt', 'w') as file:
    for row in rows:
        file.write(str(row[0]) + '\n')

# Step 5: Close the cursor and connection
cursor.close()
conn.close()
