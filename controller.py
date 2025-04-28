import re
import model
from model import *
from datetime import datetime
import pandas as pd


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

def getTable(table_name):
    # Whitelist
    whitelist = {"user", "bike", "subscription"}
    if table_name not in whitelist:
        return "ERROR: Wrong table name"
    # Open connection to database
    con = sqlite3.connect('bysykkel.db')

    # Use parameterized query to prevent SQL injection
    query = f"SELECT * FROM {table_name}"
    
    # Execute query with the table name
    df = pd.read_sql_query(query, con)
    
    # Close the connection
    con.close()

    return df

### ---------------------- TASK 3 ------------------- ####

# Starts a new trip
# Inserts a new trip into the trip table
def start_new_trip(user_id, bike_id, start_station_id):
    print(user_id)
    print(bike_id)
    print(start_station_id)
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
    if user_id is None:
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



# Stops a trip
# Updates the trip table with end_station_id and trip_end_time
# Returns trip_id as a string
def stop_trip(user_id, end_station_id, trip_id):
    update_table("trip", "trip_id", trip_id, "end_station_id", end_station_id)
    update_table("trip", "trip_id", trip_id,
                 "trip_end_time", f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

# Bike dropoff
# Updates the bike table with bike_station_id and bike_status
# Stops the trip
# Updates the trip table with end_station_id and trip_end_time
# Returns a tuple consisting of string and a bool
# The string is a message to be replied to the user, 
# Either telling what was wrong or if it operation went through
# The bool is to be used for frontend handling telling if the whole
# operation was succesfull
def bike_droppoff(user_name, end_station_name):
    # Check if user_name is valid
    user_id = get_user_id_from_user_name(user_name)
    if user_id is None:
        return ("Username do not exist", False)
    user_id = user_id[0]
    end_station_id = get_station_id_from_station_name(end_station_name)
    trip_id = trip_id = get_ongoing_trip_id_from_user_id(user_id)
    # If user has no ongoing trips
    if trip_id is None: 
        return ("User has no ongoing trips", False)
    print(trip_id)
    trip_id = trip_id[0]
    stop_trip(user_id, end_station_id, trip_id)
    print(trip_id)
    bike_id = get_bike_id_from_trip_id(trip_id)
    bike_change_status(bike_id, 'Parked')
    update_table("bike", "bike_id", bike_id, "bike_station_id", end_station_id)
    return ("Droppoff done :)", True)

def submit_complaint(user_name, complaint_type_id):
    user_id = get_user_id_from_user_name(user_name)[0]
    bike_id = get_latest_bike_id_from_user_id(user_id)
    dict = {
        "user_id": str(user_id),
        "bike_id": str(bike_id),
        "complaint_type_id": str(complaint_type_id),
        "complaint_time": f"'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'"
    }
    insert_to_table("complaint", dict)
