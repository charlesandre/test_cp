INSERT INTO cp_datawarehouse.users_daily_rides 
SELECT 
    u.user_id, 
    u.loyalty_status, 
    u.loyalty_status_txt, 
    cast(quote_date as date), 
    count(ride_id),
    SUM(r.price_nominal) 
FROM 
    cp_datawarehouse.users u 
INNER JOIN cp_datawarehouse.rides r 
    ON r.user_id = u.user_id 
GROUP BY u.user_id, cast(quote_date as date);