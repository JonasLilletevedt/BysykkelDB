SELECT
    count(station_name) AS count,
    s.station_name
FROM  
    trip AS t 
JOIN 
    end_station AS s 
    WHERE t.end_station_id == s.station_id
GROUP BY s.station_name