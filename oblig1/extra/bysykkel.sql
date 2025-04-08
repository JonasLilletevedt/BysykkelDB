
CREATE TABLE user(
    user_id INTEGER,
    user_name TEXT,
    user_phone_number TEXT,
    user_longitude FLOAT,
    user_latitude FLOAT,

    PRIMARY KEY(user_id)
);


CREATE TABLE bike(
    bike_id INTEGER,
    bike_station_id INTEGER,
    bike_status TEXT,
    bike_reperation_status TEXT,
    bike_name TEXT,

    PRIMARY KEY(bike_id),
    FOREIGN KEY(bike_station_id) REFERENCES start_station(start_station_id)
);


CREATE TABLE start_station(
    start_station_id INTEGER,
    start_station_available_spots INTEGER,
    start_station_max_spots INTEGER,
    start_station_name TEXT,
    start_station_latitude FLOAT,
    start_station_longitude FLOAT,

    PRIMARY KEY(start_station_id)
);

CREATE TABLE end_station(
    end_station_id INTEGER,
    end_station_available_spots INTEGER,
    end_station_max_spots INTEGER,
    end_station_name TEXT,
    end_station_latitude FLOAT,
    end_station_longitude FLOAT,

    PRIMARY KEY(end_station_id)
);

CREATE TABLE subscription(
    subscription_id INTEGER,
    subscription_user_id INTEGER,
    subscription_status TEXT,
    subscription_start_time DATE,
    subscription_end_time DATE,
    subscription_type Text,

    PRIMARY KEY(subscription_id),
    FOREIGN KEY(subscription_user_id) REFERENCES user(user_id)
);

CREATE TABLE trip(
    trip_id INTEGER,
    trip_user_id INTEGER,
    trip_bike_id INTEGER,
    trip_start_station_id INTEGER,
    trip_end_station_id INTEGER,
    trip_start_time DATE,
    trip_end_time DATE,

    PRIMARY KEY(trip_id),
    FOREIGN KEY(trip_user_id) REFERENCES user(user_id),
    FOREIGN KEY(trip_bike_id) REFERENCES bike(bike_id),
    FOREIGN KEY(trip_start_station_id) REFERENCES start_station(start_station_id),
    FOREIGN KEY(trip_end_station_id) REFERENCES end_station(end_station_id)
);

