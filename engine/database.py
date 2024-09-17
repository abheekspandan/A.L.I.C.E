import mysql.connector
import csv

try:
    # Connect to MySQL
    con = mysql.connector.connect(
        host="localhost",  # Change to your host
        user="ALICE",  # Change to your MySQL username
        password="krusanali",  # Change to your MySQL password
        database="alice"  # Change to your database name
    )

    cursor = con.cursor()

    # Create table sys_command
    query = """CREATE TABLE IF NOT EXISTS sys_command (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(100),
                   path VARCHAR(1000)
               )"""
    cursor.execute(query)

    # Optionally insert a record (uncomment if needed)
    # query = r"INSERT INTO sys_command (name, path) VALUES ('VS Code', 'E:\\Microsoft VS Code\\Code.exe')"
    # cursor.execute(query)
    # con.commit()

    # Create table web_command
    query = """CREATE TABLE IF NOT EXISTS web_command (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(100),
                   url VARCHAR(1000)
               )"""
    cursor.execute(query)

    # Insert a record (uncomment if needed)
    # query = """INSERT INTO web_command (name, url) VALUES ('youtube', 'https://www.youtube.com/')"""
    # cursor.execute(query)
    # con.commit()

    # Create table contacts
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(200),
                       mobile_no VARCHAR(255)
                   )''')

    # Specify the column indices you want to import (0-based index)
    # Example: Importing the 1st and 3rd columns (ensure these indices are correct for your CSV)
    desired_columns_indices = [0, 20]

    # Read data from CSV and insert into MySQL table for the desired columns
    # with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     for row in csvreader:
    #         # Ensure that the row has enough columns to avoid IndexError
    #         if len(row) > max(desired_columns_indices):
    #             selected_data = [row[i] for i in desired_columns_indices]
    #             # Insert data into the table using MySQL's parameterized query syntax
    #             cursor.execute('''INSERT INTO contacts (name, mobile_no) VALUES (%s, %s);''', tuple(selected_data))

    # # Commit changes
    # con.commit()

#     # this code down below is there to check whether a particular person's entry is present in the contacts table
#     query = 'Atharva'
#     query = query.strip().lower()

# # Correct query with both placeholders accounted for
    # cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE '%Atharva%' OR LOWER(name) LIKE 'Atharva%'")
    # results = cursor.fetchall()
    # print(results[0][0])

# # Check if any results were found before accessing the first item
#     if results:
#     # Display the mobile number of the first result
#         print(results[0][0])
#     else:
#         print("No results found.")


except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if con:
        con.close()
