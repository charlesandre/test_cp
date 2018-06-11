/*1 Creating and populate table */
CREATE TABLE cp_datawarehouse.users_daily_rides (
  user_id text,
  loyalty_status int,
  loyalty_status_txt text,
  daily_date date,
  nb_rides int,
  total_price numeric,
  PRIMARY KEY (user_id, daily_date)
);

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


/*2 Average basket per day*/
SELECT user_id, cast(quote_date as date), AVG(price_nominal)FROM cp_datawarehouse.rides
WHERE state = 'completed'
GROUP BY cast(quote_date as date), user_i;


/*3 5 days with the least number of completed ride */
SELECT cast(quote_date as date) as day, COUNT(ride_id) as nb_of_ride 
FROM cp_datawarehouse.rides
WHERE state = 'completed'
GROUP BY cast(quote_date as date)
ORDER BY COUNT(ride_id) ASC
LIMIT 5;