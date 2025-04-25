import sqlite3

from datetime import datetime

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
        ON b.bike_station_id = s.station_id
    WHERE
        b.bike_status = 'Parked'
        AND s.station_name = '{station_name}'
    LIMIT 
        1
    """

    table = pd.read_sql_query(sql_command, con)
    res =  table["bike_id"].tolist() + table["bike_name"].tolist()

    return res 

def bike_change_status(db_path, bike_id, bike_status):
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

def bike_checkout(db_path, bike_id):
    bike_change_status(db_path, bike_id, "Active")





def get_user_id_from_user_name(db_path, user_name):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    SELECT
        user_id
    FROM 
        user
    WHERE
        user_name = ?
    """

    user_id = cur.execute(sql_command, (user_name,)).fetchone()[0]
    con.commit()

    return str(user_id)

def get_station_id_from_station_name(db_path, station_name):
    # Connection to db
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql_command = f"""
    SELECT
        station_id
    FROM 
        station
    WHERE
        station_name = ?
    """

    station_id = cur.execute(sql_command, (station_name,)).fetchone()[0]
    con.commit()

    return str(station_id)


def start_new_trip(db_path, user_id, bike_id, start_station_id):
    dict = {
        "user_id": str(user_id),
        "bike_id": str(bike_id),
        "start_station_id": str(start_station_id),
        "trip_start_time": f"'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'"
    }
    insert_to_table("trip", dict, db_path)


def get_trip_id_from_user_id(db_path, user_id):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    sql_command = f"""
    SELECT
        t.trip_id
    FROM 
        trip AS t
    JOIN user AS u 
        ON t.user_id = u.user_id
    WHERE
        t.end_station_id IS NULL 
        AND u.user_id = ? 
    """
    
    cur.execute(sql_command, (user_id))
    res = cur.fetchone()[0]
    con.commit()

    return str(res)

def get_bike_id_from_trip_id(db_path, trip_id):
    con = sqlite3.connect(db_path) 
    cur = con.cursor()

    sql_command = f"""
    SELECT
        bike_id
    FROM 
        trip
    WHERE
        trip_id = ?
    """
    cur.execute(sql_command, (trip_id,))
    res = cur.fetchone()[0]
    con.commit()
    return str(res)


def update_table(db_path, table, id_name, id_value, attribute_name, value):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    sql_command = f"""
    UPDATE
        `{table}`
    SET
        `{attribute_name}` = ?
    WHERE
        `{id_name}` = ?
    """

    cur.execute(sql_command, (value, id_value))
    con.commit()


def stop_trip(db_path, user_id, end_station_id):
    trip_id = get_trip_id_from_user_id(db_path, user_id)
    update_table(db_path, "trip", "trip_id", trip_id, "end_station_id", end_station_id)
    update_table(db_path, "trip", "trip_id", trip_id,
                 "trip_end_time", f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    return str(trip_id)

def bike_droppoff(db_path, user_name, end_station_name):
    user_id = get_user_id_from_user_name(db_path, user_name)
    end_station_id = get_station_id_from_station_name(db_path, end_station_name)
    trip_id = stop_trip(db_path, user_id, end_station_id)
    bike_id = get_bike_id_from_trip_id(db_path, trip_id)
    bike_change_status(db_path, bike_id, 'Parked')
    update_table(db_path, "bike", "bike_id", bike_id, "bike_station_id", end_station_id)

#bike_change_status("bysykkel.db", 1, "Parked")
#bike_change_status("bysykkel.db", 2, "Parked")
#bike_change_status("bysykkel.db", 3,"Parked")
#bike_change_status("bysykkel.db", 4, "Parked")
#bike_change_status("bysykkel.db", 5, "Parked")
#bike_change_status("bysykkel.db", 6, "Parked")
#bike_change_status("bysykkel.db", 7, "Parked") 




# test_insert_to_table
# d = {
#         "user_name" : "'meg'",
#         "user_phone_number" : "1222222222'",
#         "user_email" : "'@@@@@t@@@@@'"
#         }

# insert_to_table("user", d, "bysykkel.db")

