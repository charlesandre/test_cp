"""
test_load
"""
# pylint: disable=too-few-public-methods,line-too-long,invalid-name

import psycopg2

from cp_datawarehouse.config.base import config
from cp_datawarehouse.etl.load import (
    insert_users_list,
    insert_rides_list,
    insert_users_daily_rides
)
from tests.tools.db_init import initialize_database

CONFIG = config()


def test_insert_users_list():
    """
    Test INSERT of a dummy CSV into users database table
    """

    initialize_database(drop=True)

    users_list = [
        ('user_id', 'loyalty_status', 'loyalty_status_txt'),
        (1, 0, 'red'),
        (3, 3, 'platinum'),
        (4, 1, 'silver'),
        (2, 2, 'gold'),
    ]

    insert_users_list(users_list)

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.users")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == users_list[1:].sort()

def test_insert_rides():

    initialize_database(drop=True)

    rides_list = [
        ('ride_id', 'user_id', 'from_zipcode', 'to_zipcode', 'state', 'quote_date', 'completed_date', 'price_nominal', 'loyalty_point_earned' 'loyalty_status', 'loyalty_status_txt'),
        (1, 1, '75012', '75011', 'completed', '2018-03-31 04:25:45.582', '2018-04-12 04:25:45.582', 5.5, 1),
        (2, 2, '75013', '75016', 'completed', '2018-03-21 04:25:45.582', '2018-03-22 04:25:45.582', 5.5, 1),
        (3, 3, '75014', '75015', 'completed', '2018-02-20 04:25:45.582', '2018-03-02 04:25:45.582', 5.5, 1),
    ]

    insert_rides_list(rides_list)

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.rides")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == rides_list[1:].sort()

def test_insert_users_daily_rides():

    initialize_database(drop=True)

    users_daily_rides_list = [
        ('user_id', 'loyalty_status', 'loyalty_status_txt', 'daily_date', 'nb_rides', 'total_price'),
        (1, 1, 'red', '2018-03-21', '10', 1),
        (2, 2, 'plat', '2018-03-22', '20', 3),
        (3, 3, 'blue', '2018-03-23', '12', 6),
    ]

    insert_users_daily_rides(users_daily_rides_list)

    conn = psycopg2.connect(CONFIG["postgres_url"])

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cp_datawarehouse.users_daily_rides")
        result = cur.fetchall()

    # Skip CSV header first line
    assert result.sort() == users_daily_rides_list[1:].sort()