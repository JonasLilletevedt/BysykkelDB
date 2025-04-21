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

    sql_command = f"""
    SELECT
        count(station_name) AS count,
        s.station_name
    FROM  
        trip AS t 
    JOIN 
        station AS s 
        WHERE t.end_station_id == s.station_id
    GROUP BY
        s.station_name
    """

    table = pd.read_sql_query(sql_command, con)

    return table


def get_available_bikes_based_on_station_and_bike_name(db_path, filter_station, filter_bike):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    SELECT
        s.station_id,
        s.station_name,
        b.bike_name
    FROM 
        bike AS b
    INNER JOIN 
        station AS s
        ON b.bike_station_id == s.station_id
    WHERE
        b.bike_status = 'Parked'
        AND s.station_name LIKE '%{filter_station}%'
        AND b.bike_name LIKE '%{filter_bike}%'
    """

    table = pd.read_sql_query(sql_command, con)

    return table

def get_station_names(db_path):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    SELECT
        station_name FROM station
    """

    table = pd.read_sql_query(sql_command, con)

    data = pd.DataFrame.to_dict(table)["station_name"]
    res = {}
    for value in data.values():
        res[value] = value
    return res

def get_first_available_bike(db_path, station_name):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    SELECT
        b.bike_id,
        b.bike_name
    FROM 
        bike AS b
    INNER JOIN 
        station AS s
        ON b.bike_station_id == s.station_id
    WHERE
        b.bike_status = 'Parked'
        AND s.station_name == '{station_name}'
    LIMIT 
        1
    """

    table = pd.read_sql_query(sql_command, con)
    res =  table["bike_id"].tolist() + table["bike_name"].tolist()

    return res

def bike_checkout(db_path, bike_id, bike_status):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    UPDATE
        bike
    SET
        bike_status = ?
    WHERE 
        bike_id = ?
    """

    cur.execute(sql_command, (bike_status,bike_id))
    con.commit()


# test_insert_to_table
# d = {
#         "user_name" : "'meg'",
#         "user_phone_number" : "1222222222'",
#         "user_email" : "'@@@@@t@@@@@'"
#         }

# insert_to_table("user", d, "bysykkel.db")

