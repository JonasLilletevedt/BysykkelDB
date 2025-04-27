import re
import sqlite3
import help_sql_commands
from help_sql_commands import *
from datetime import datetime
import pandas as pd
from shiny.ui import insert_accordion_panel


path = "bysykkel.db"
### --------------------- TASK 1 ------------------- ####

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

### ---------------------- TASK 2 ------------------- ####

# Gets all stations in db
# Returns a pd.dataframe
def get_trips_ended_on_all_stations():
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
    sql_command = f"""
    SELECT
        s.station_name AS "Station Name",
        COUNT(*) AS "Trips ended at station"
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

# Gets available bikes in a station based on station name and bike name
# Returns a pd.dataframe
def get_available_bikes_based_on_station_and_bike_name(filter_station, filter_bike):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
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
    # Returns a pd.dataframe
    return table


### ---------------------- TASK 3 ------------------- ####

def get_station_names():
    # Connection to db
    con = sqlite3.connect(path)
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

# Gets first available bike in station
def get_first_available_bike(station_name):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query    
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
    # Returns a list with bike_id and bike_name
    return res 

#Changes bike status
def bike_change_status(bike_id, bike_status):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
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

# Gets user_id from user_name
# Returns a string
def get_user_id_from_user_name(user_name):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
    sql_command = f"""
    SELECT
        user_id
    FROM 
        user
    WHERE
        user_name = ?
    """
    user_id = cur.execute(sql_command, (user_name,)).fetchone()
    con.commit()
    # Returns user_id as a string
    return user_id

# Gets station_id from station_name
# Returns a string
def get_station_id_from_station_name(station_name):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
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
    # Returns station_id as a string
    return str(station_id)

# Starts a new trip
# Inserts a new trip into the trip table
def start_new_trip(user_id, bike_id, start_station_id):
    # Dictionary with values to insert
    dict = {
        "user_id": str(user_id),
        "bike_id": str(bike_id),
        "start_station_id": str(start_station_id),
        "trip_start_time": f"'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'"
    }
    # Inserts the trip into the trip table
    insert_to_table("trip", dict)

# Bike checkout
# Updates the bike table with bike_station_id and bike_status
# Starts a new trip
# Updates the trip table with start_station_id and trip_start_time
def bike_checkout(user_name, station_name):
    user_id = get_user_id_from_user_name(user_name)
    # If user name does not exist
    if user_id == 'None':
        return "Username do not exist, please register, or check your spelling"
    user_id = user_id[0]
    available_bike = get_first_available_bike(station_name)
    # If no bike is available
    if len(available_bike) == 0:
        return "No bike available at station"
    # id [0]
    bike_id = available_bike[0]
    # name[1]
    bike_name = available_bike[1]
    station_id = get_station_id_from_station_name(station_name) 
    # Change bike status to "Active" after checking bike exists,
    # user exists and able to get station id
    bike_change_status(bike_id, "Active")
    # Start new trip
    start_new_trip(user_id, bike_id, station_id)
    return f"Checkout succesfull :) \n Collect your bike: {bike_name}"


# Gets trip_id from bike_id
# Returns a string
def get_ongoing_trip_id_from_user_id(user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
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
    res = cur.fetchone()
    con.commit()
    # Returns trip_id as a string
    return str(res)

# Gets bike_id from trip_id
# Returns a string
def get_bike_id_from_trip_id(trip_id):
    con = sqlite3.connect(path) 
    cur = con.cursor()
    # SQL query
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
    # Returns bike_id as a string
    return str(res)

# Stops a trip
# Updates the trip table with end_station_id and trip_end_time
# Returns trip_id as a string
def stop_trip(user_id, end_station_id):
    trip_id = get_ongoing_trip_id_from_user_id(user_id)
    update_table("trip", "trip_id", trip_id, "end_station_id", end_station_id)
    update_table("trip", "trip_id", trip_id,
                 "trip_end_time", f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    # Returns trip_id as a string
    return str(trip_id)

# Bike dropoff
# Updates the bike table with bike_station_id and bike_status
# Stops the trip
# Updates the trip table with end_station_id and trip_end_time
def bike_droppoff(user_name, end_station_name):
    # Check if user_name is valid
    user_id = get_user_id_from_user_name(user_name)
    if user_id == 'None':
        return "Username do not exist"
    user_id = user_id[0]
    end_station_id = get_station_id_from_station_name(end_station_name)
    trip_id = stop_trip(user_id, end_station_id)
    # If user has no ongoing trips
    if trip_id == 'None': 
        return "User has no ongoing trips"
    bike_id = get_bike_id_from_trip_id(trip_id)
    bike_change_status(bike_id, 'Parked')
    update_table("bike", "bike_id", bike_id, "bike_station_id", end_station_id)
    return "Droppoff done :)"

# Gets available spots in a station, if on trip 
# gets avialable park spots
# if looking for a bike, gets available bikes
# Also returns a map link
# Returns a pd.dataframe
def get_available_spots(station_name, get_or_park):
    station_id = get_station_id_from_station_name(station_name)
    con = sqlite3.connect(path) 
    # SQL query
    sql_command = f"""
    SELECT
        s.station_name AS "Station Name",
        CAST(
            CASE
                WHEN ? = 'get' THEN
                    (COUNT(b.bike_id) * 100 / s.max_spots)
                WHEN ? = 'park' THEN
                    ((s.max_spots - COUNT(b.bike_id)) * 100 / s.max_spots)
            END
        AS TEXT) || '%' AS "Available Spots",
        'https://www.openstreetmap.org/#map=17/'|| CAST(s.latitude AS TEXT) || '/' || CAST(s.longitude AS TEXT) AS MAP
    FROM
        station AS s
    LEFT JOIN bike AS b ON
        b.bike_station_id = s.station_id AND b.bike_status = 'Parked'
    WHERE
        s.station_id = ?
    GROUP BY 
        s.station_id
    """
    table = pd.read_sql_query(sql_command, con, params=(get_or_park, get_or_park, station_id,))
    # Returns a pd.dataframe
    return table
