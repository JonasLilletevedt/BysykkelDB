SELECT
        t.trip_id
    FROM 
        trip as t
    JOIN user as u 
        ON u.user_id = t.user_id
    JOIN bike as b 
        ON b.bike_id = t.bike_id
    WHERE
         u.user_id = ? AND 
         t.end_station_id IS NULL AND 
         b.bike_id = ? AND b.bike_status = 'Active'