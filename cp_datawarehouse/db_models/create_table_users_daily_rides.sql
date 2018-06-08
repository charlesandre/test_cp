CREATE TABLE cp_datawarehouse.users_daily_rides (
  user_id text,
  loyalty_status int,
  loyalty_status_txt text,
  daily_date date,
  nb_rides int,
  total_price numeric,
  PRIMARY KEY (user_id, daily_date)
);