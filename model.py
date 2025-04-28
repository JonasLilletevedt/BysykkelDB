import sqlite3
import pandas as pd

path = "bysykkel.db"

# Inserts to table
def insert_to_table(table, dict_attributes_values):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    # Sql command, input to sqlite
    sql_command = f"INSERT INTO {table} ({",".join(list(dict_attributes_values.keys()))}) VALUES ({",".join(list(dict_attributes_values.values()))});" 
    try:
        cur.execute(sql_command)
        print("Added to db")
        print(sql_command)
        # Commits
        con.commit()
        return True
    except:
        print("Not added")
        print(sql_command)
        return False


### ----------------- TASK1 ------------------ ###
def search_table(search, table, main_attr, attributes):
    attr = ",".join(attributes) 
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    sql_command = f"SELECT {attr} FROM {table} WHERE {main_attr} LIKE '%{search}%';"
    table = pd.read_sql_query(sql_command, con)
    return table


def update_table(table, id_name, id_value, attribute_name, value):
    con = sqlite3.connect(path)
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


### ---------------- TASK2 ------------------ ###
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


### ---------------------- TASK 3 ------------------- ####

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
    cur.execute(sql_command, (user_id,))
    res = cur.fetchone()
    con.commit()
    # Returns trip_id as a string
    return res

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

# Gets all complaint types 
def get_complaint_types_and_id():
    con = sqlite3.connect(path)
    cur = con.cursor()
    # SQL query
    sql_command = f"""
    SELECT
        *
    FROM
        complaint_types
    """
    cur.execute(sql_command,)
    data = cur.fetchall()
    res = {}
    for t in data:
        res[t[0]] = t[1]
    return res

### --------------- TASK4 ---------------- ###
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

# Gets coordinates from station_name
def get_cordinates(station_name):
    spørring ="""
    SELECT 
        latitude,
        longitude
    FROM
        Station
    WHERE
        station_name = ?;
    """

    con = sqlite3.connect(path)
    res = pd.read_sql_query(spørring,con,params=(station_name,))
    res = pd.DataFrame.to_dict(res)
    return tuple((res["latitude"][0], res["longitude"][0]))

# Gets users latest bike_id 
def get_latest_bike_id_from_user_id(user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()
    sql_command = f"""    
    SELECT 
        bike_id
    FROM
        trip
    WHERE
        user_id = ?
    ORDER BY 
        trip_id DESC
    LIMIT 
        1
    """
    cur.execute(sql_command,(user_id,))
    return cur.fetchone()[0]

