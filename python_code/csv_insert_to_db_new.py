#!/usr/bin/env python3
import sqlite3
import csv
import os

# If it was not downloaded directly from git, it may not have preserved the executable 
# permission. You can run the following command to give it the permission: 
# "chmod +x csv_insert_to_db_new.py" in the terminal

#This script reads a CSV file and inserts the values into a SQLite database.
# It assumes that the CSV file has a header with with the colum names, 
# if not you can add this manually. It also ssumes that the SQLite database has
# tables with the same names as the CSV columns.
# Lastly you will either need to change the path to the CSV file and the path of
# the database to match your own file paths. 

# Get valid path for database and CSV file
# Checks if path is valid
def get_valid_path(prompt, file_extension):
    while True:
        path = input(prompt)
        if os.path.exists(path) and path.endswith(file_extension):
            return path
        print(f"Error: File not found or wrong file type. Please check that the file exists and is a {file_extension} file.")

# Database path
# If you want to run python in in vscode 
# and add paths directly to the py script 
# you can uncomment the following lines

# #path_db = "bysykkel_new.db"
# CSV file path
#path_csv = "bysykkel.csv"
#con = sqlite3.connect(path_db)
#cur = con.cursor()

# Get all tables in the database
def get_tables():
    result = []
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    for t in tables:
        result.append(t[0])
    return result

# Get the attributes from a table
def get_attributes_from_table(table):
    attributes = []
    cur.execute(f"SELECT * FROM {table} LIMIT 1;")
    for attribute in cur.description:
        attributes.append(attribute[0])
    return attributes

# Get the column names and types for a table
def get_column_types(table):
    types = {}
    cur.execute(f"PRAGMA table_info({table});")
    for col in cur.fetchall():
        # col[1] is name, col[2] is type
        types[col[1]] = col[2].upper()
    return types

def convert_value(value, sqlite_type):
    if value == '':
        return None
    
    try:
        if sqlite_type == 'INTEGER':
            return int(value)
        elif sqlite_type == 'REAL':
            return float(value)
        elif sqlite_type == 'TEXT':
            return str(value)
        elif sqlite_type == 'DATETIME':
            return value
        else:
            # Default to string for unknown types
            return str(value) 
    except ValueError:
        return None

def formatter(attributes):
    streng = ""
    for attribute in attributes:
         streng += f"\"{attribute}\"" + ","
    return streng[:-1]

def read_CSV():
    with open(path_csv, "r") as f:
        reader = csv.reader(f)
        return list(reader)
    
# Returns a tuple
# [0] for attributes
# [1] for values
def get_all_values_in_row(index, attributes):
    values = []
    nyeAt = []
    head = read_CSV()
    
    # Get the table name from the first attribute (assuming it's in format table.column)
    table_name = attributes[0].split('.')[0]
    column_types = get_column_types(table_name)
    
    for i in range(0, len(head[0])):
        if head[0][i] in attributes:
            nyeAt.append(head[0][i])
            # Get the SQLite type for this column
            sqlite_type = column_types.get(head[0][i], 'TEXT')
            # Convert the value based on the SQLite type
            value = convert_value(head[index][i], sqlite_type)
            values.append(value)
    return tuple((nyeAt, values))

# Get number of rows in the CSV file
def get_rows():
    head = read_CSV()
    count = 0
    for line in head:
        count += 1
    return count

# Insert all rows containing values from the CSV file to the table
def insert_to_table(table):
    columns = get_attributes_from_table(table)
    columns = formatter(columns)

    size = get_rows()
    row_index = 1
    while row_index < size:
        try:
            # Get attributes and values for the current row
            attributes, values = get_all_values_in_row(row_index, get_attributes_from_table(table))
            
            # Skip if all values are None
            if all(value is None for value in values):
                row_index += 1
                continue
            
            # Create placeholders for the values
            placeholders = ','.join(['?' for _ in values])
            
            # Create the SQL query with placeholders using INSERT OR REPLACE
            query = f"INSERT OR REPLACE INTO {table} ({','.join(attributes)}) VALUES ({placeholders})"
            
            # Execute the query with values as parameters
            cur.execute(query, values)
            con.commit()

        except Exception as e:
            print(f"Error inserting row {row_index}: {str(e)}")
            print(f"Values: {values}")  # Print the values for debugging
        row_index += 1

# Inserts all values from the CSV file to theire respected table in the database
def insert_to_all_tables():
    tables = get_tables()
    for t in tables:
        insert_to_table(f"\"{t}\"")

# Main function
# Can run from terminal or as a script
if __name__ == "__main__":
    # Get paths when running as main script
    print("Please enter the full path to your files:")
    path_db = get_valid_path("Path to database (.db): ", ".db")
    path_csv = get_valid_path("Path to CSV file (.csv): ", ".csv")

    print(f"\nUsing the following files:")
    print(f"Database: {path_db}")
    print(f"CSV file: {path_csv}")

    try:
        con = sqlite3.connect(path_db)
        cur = con.cursor()
        insert_to_all_tables()
        print("\nInsertion completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("This script was made by @jolil6835@uib.no")
        input("\nPress Enter to exit...")  

