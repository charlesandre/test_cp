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
            'from_zipcode' : [75019, 91017],
            'to_zipcode' : [75018, 75001],
            'state' : ['not_completed', 'completed'],
            'price_nominal' : [4.56, 5.05],
            'loyalty_points_earned' : [0, 5],
        })[order],
        check_names=True
    )
