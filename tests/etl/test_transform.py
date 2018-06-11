"""
test_load
"""
# pylint: disable=too-few-public-methods,line-too-long,invalid-name

import io

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from cp_datawarehouse.etl.transform import (
    clean_users_csv,
    clean_rides_csv,
    create_users_daily_rides_df,
    get_5_days_with_least_rides,
    get_average_basket,
    create_chart_df,
)


def test_clean_users_csv():
    """
    Test INSERT of a dummy CSV into users database table
    """

    users_csv = io.StringIO('user_id,loyalty_status,loyalty_status_txt\n1,0,red\n2,1,silver\n3,2,gold\n4,3,platinium\n5,3,platinum')

    clean_users_df = clean_users_csv(users_csv)

    assert_frame_equal(
        clean_users_df.sort_index(axis=1),
        DataFrame({
            'user_id' : [1, 2, 3, 4, 5],
            'loyalty_status' : [0, 1, 2, 3, 3],
            'loyalty_status_txt' : ['red', 'silver', 'gold', 'platinum', 'platinum'],
        }).sort_index(axis=1),
        check_names=True
    )


def test_clean_rides_csv():
    
    rides_csv = io.StringIO('ride_id,from_zipcode,to_zipcode,state,price_nominal,loyalty_points_earned\n7cd8b375f4577f99414aae0825ecd611,75019,75018,not_completed,4.56,0\n565b09d786159420be7e8e1058ea76ae,01017,75001,completed,5.05,5\n565b09d786159420be7e8e1058ea76ae,91017,75001,completed,5.05,5\n9691cb806a1d22ba1d553d344326f357,69008,69004,not_completed,6.75,0')

    clean_rides_df = clean_rides_csv(rides_csv)
    order = ['ride_id', 'from_zipcode', 'to_zipcode', 'state', 'price_nominal', 'loyalty_points_earned']
    assert_frame_equal(
        clean_rides_df[order],
        DataFrame({
            'ride_id' : ['7cd8b375f4577f99414aae0825ecd611', '565b09d786159420be7e8e1058ea76ae'],
            'from_zipcode' : ['75019', '91017'],
            'to_zipcode' : ['75018', '75001'],
            'state' : ['not_completed', 'completed'],
            'price_nominal' : [4.56, 5.05],
            'loyalty_points_earned' : [0, 5],
        })[order],
        check_names=True
    )

def test_users_daily_rides():
    rides_csv = io.StringIO('ride_id,user_id,state,quote_date,price_nominal\n100,u1,completed,2018-05-31 08:13:29.171,12\n101,u1,completed,2018-05-31 09:13:29.171,8\n102,u1,completed,2018-06-01 08:17:29.171,20\n103,u2,completed,2018-05-31 08:13:29.171,5')
    users_csv = io.StringIO('user_id,loyalty_status,loyalty_status_txt\nu1,0,red\nu2,1,silver\nu3,2,gold\nu4,3,platinium\nu5,3,platinum')

    users_daily_rides = create_users_daily_rides_df(users_csv, rides_csv)
    order = ['user_id', 'daily_date', 'nb_rides', 'total_price', 'loyalty_status', 'loyalty_status_txt']
    assert_frame_equal(
        users_daily_rides[order],
        DataFrame({
            'user_id' : ['u1', 'u1', 'u2'],
            'loyalty_status' : [0, 0, 1],
            'loyalty_status_txt' : ['red', 'red', 'silver'],
            'daily_date' : ['2018-05-31', '2018-06-01', '2018-05-31'],
            'nb_rides' : [2, 1, 1],      
            'total_price' : [20, 20, 5],
        })[order],
        check_dtype=False,
        check_names=True
    )
def test_get_5_day_with_least_rides():
    rides_csv = io.StringIO('ride_id,user_id,state,quote_date,price_nominal\n99,u1,completed,2018-05-31 08:13:29.171,12\n100,u1,completed,2018-05-31 08:13:29.171,12\n101,u1,completed,2018-05-31 09:13:29.171,8\n102,u1,completed,2018-05-31 08:17:29.171,20\n103,u2,completed,2018-06-01 08:13:29.171,5\n104,u2,completed,2018-06-01 08:13:29.171,5\n105,u2,completed,2018-06-01 08:13:29.171,5\n106,u2,completed,2018-06-03 08:13:29.171,5\n119,u2,completed,2018-06-03 08:13:29.171,5\n115,u2,completed,2018-06-03 08:13:29.171,5\n117,u2,completed,2018-06-03 08:13:29.171,5\n116,u2,completed,2018-06-03 08:13:29.171,5\n107,u2,not_completed,2018-06-04 08:13:29.171,5\n108,u2,completed,2018-06-04 08:13:29.171,5\n109,u2,completed,2018-06-05 08:13:29.171,5\n110,u2,completed,2018-06-05 08:13:29.171,5')
    least_5_days = get_5_days_with_least_rides(rides_csv)
    assert_frame_equal(
        least_5_days,
        DataFrame({
            'day' : ['2018-06-04', '2018-06-05', '2018-06-01', '2018-05-31', '2018-06-03'],
            'nb_rides' : [1, 2, 3, 4, 5],        
        }),
        check_dtype=False,
        check_names=True
    )

def test_get_average_basket():
    rides_csv = io.StringIO('ride_id,user_id,state,quote_date,price_nominal\n99,u1,completed,2018-05-31 08:13:29.171,10\n100,u1,completed,2018-05-31 08:13:29.171,20\n101,u1,completed,2018-05-31 09:13:29.171,10\n102,u1,completed,2018-05-31 08:17:29.171,20\n112,u1,completed,2018-06-01 08:17:29.171,15\n112,u1,completed,2018-06-01 08:17:29.171,25\n112,u1,completed,2018-06-01 08:17:29.171,20')
    average_basket = get_average_basket(rides_csv)
    order = ['day', 'avg_price']
    assert_frame_equal(
        average_basket[order],
        DataFrame({
            'day' : ['2018-05-31', '2018-06-01'],
            'avg_price' : [15.0, 20.0],        
        })[order],
        check_dtype=False,
        check_names=True
    )


def test_create_chart_df():
    rides_csv = io.StringIO('ride_id,user_id,state,quote_date,price_nominal\n100,u1,completed,2018-05-31 08:13:29.171,12\n101,u1,completed,2018-05-31 09:13:29.171,8\n102,u1,completed,2018-06-01 08:17:29.171,20\n103,u2,completed,2018-05-31 08:13:29.171,5')
    users_csv = io.StringIO('user_id,loyalty_status,loyalty_status_txt\nu1,0,red\nu2,1,silver\nu3,2,gold\nu4,3,platinium\nu5,3,platinum')

    chart_df = create_chart_df(rides_csv, users_csv)
    order = ['week_number', 'loyalty_status', 'loyalty_status_txt', 'nb_rides']
    assert_frame_equal(
        chart_df[order],
        DataFrame({
            'week_number' : [22, 22],
            'loyalty_status' : [0, 1],
            'loyalty_status_txt' : ['red', 'silver'],
            'nb_rides' : [3, 1]        
        })[order],
        check_names=True
    )