import sqlite3

import pandas as pd
from shiny.ui import insert_accordion_panel

# Checks if username is valid
# name should only contain letters
def check_valid_name(name):
    if len(name) == 0:
        return False
    letters = "abcdefghijklmnopqrstuvwxyz"
    for c in name.lower():
        if c not in letters:
            return False
    return True

# Checks if phonenumber is valid
# phonenumber should be exactly 9 digits and only contain digits
def check_phone_number(phone_number):
    phone_number = str(phone_number)

    if len(phone_number) != 8:
        return False
    
    digits = "0123456789"
    for d in phone_number:
        if d not in digits:
            return False
    return True


# Checks if email is valid
# email should contain '@'
def check_valid_email(email):
    return '@' in email

# Inserts to table
def insert_to_table(table, dict_attributes_values, db_path):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Sql command, input to sqlite
    sql_command = f"INSERT INTO {table} ({",".join(list(dict_attributes_values.keys()))}) VALUES ({",".join(list(dict_attributes_values.values()))});" 
    try:
        cur.execute(sql_command)
        print("Added to db")
        # Commits
        con.commit()
        return True
    except:
        print("Not added")
        print(sql_command)
        return False
    
def search_table(search, table, main_attr, attributes, db_path):
    attr = ",".join(attributes) 
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql_command = f"SELECT {attr} FROM {table} WHERE {main_attr} LIKE '%{search}%';"
    table = pd.read_sql_query(sql_command, con)

    return table


def get_trips_ended_on_all_stations(db_path):
        
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = """
    SELECT
        count(station_name) AS count,
        s.station_name
    FROM  
        trip AS t 
    JOIN 
        station AS s 
        WHERE t.end_station_id == s.station_id
    GROUP BY s.station_name
    """

    table = pd.read_sql_query(sql_command, con)
    
    return table

print(get_trips_ended_on_all_stations("bysykkel.db"))

print(search_table("han", "user", "user_name", ["user_name", "user_phone_number"], "bysykkel.db"))

# test_insert_to_table
# d = {
#         "user_name" : "'meg'",
#         "user_phone_number" : "1222222222'",
#         "user_email" : "'@@@@@t@@@@@'"
#         }

# insert_to_table("user", d, "bysykkel.db")

