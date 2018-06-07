"""
Transform module provides functions to transform and clean data before further import into cp_datawarehouse tables
"""

import csv
import logging
import io

import pandas as pd


LOGGER = logging.getLogger(__name__)


def clean_users_csv(users_csv, delimiter=','):
    """
    Clean user CSV file values replacing mispelled 'platinium' values into 'platinum'.
    :param list users_csv: the CSV object (path or StringIO) WHICH INCLUDES HEADER ROW
    :return: the cleaned csv as a Pandas dataframe
    """

    users_df = pd.read_csv(users_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=users_df.shape
    ))

    users_df['loyalty_status_txt'].replace('platinium', 'platinum', inplace=True)

    return users_df




def clean_rides_csv(rides_csv, delimiter=','):
    """
    This function cleans the rides csv file by removing the rides which are not in 'Ile de France'
    """
    array_idf = ['75', '77', '78', '91', '92', '93', '94', '95'] 
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    rides_df.from_zipcode = rides_df.from_zipcode.astype(str)
    rides_clear_df = rides_df[rides_df.from_zipcode.str[:2].isin(array_idf) == True]
    rides_clear_df.from_zipcode = rides_clear_df.from_zipcode.astype(int)
    rides_clear_df.reset_index(inplace=True, drop=True)
    return rides_clear_df