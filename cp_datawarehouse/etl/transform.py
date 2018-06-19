"""
Transform module provides functions to transform and clean data before further import into cp_datawarehouse tables
"""

import csv
import logging
import io

import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
    rides_df.to_zipcode = rides_df.to_zipcode.astype(str)
    rides_clear_df = rides_df[rides_df.from_zipcode.str[:2].isin(array_idf) == True]
    rides_clear_df.reset_index(inplace=True, drop=True)
    return rides_clear_df


def get_average_basket(rides_csv='raw_data/rides.csv', delimiter=','):
    #Read CSV into pandas Dataframe.
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=rides_df.shape
    ))
    
    rides_df['day'] = pd.to_datetime(rides_df['quote_date']).dt.normalize().astype(str)[rides_df.state == 'completed']
    avg_df = rides_df.groupby(['day']).mean().reset_index().rename(columns={'price_nominal':'avg_price'})[['day', 'avg_price']]
    return avg_df

def get_5_days_with_least_rides(rides_csv='raw_data/rides.csv', delimiter=','):
    #Read CSV into pandas Dataframe.
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=rides_df.shape
    ))
    completed_rides_df = rides_df[rides_df.state == 'completed']
    completed_rides_df.loc[:, 'quote_date'] = pd.to_datetime(completed_rides_df['quote_date']).dt.normalize().astype(str)
    days_df = completed_rides_df.groupby(['quote_date']).count().sort_values('ride_id').reset_index().rename(columns={'quote_date':'day','ride_id':'nb_rides'})[['day', 'nb_rides']].head()
    return days_df


def create_users_daily_rides_df(users_csv='raw_data/users.csv', rides_csv='raw_data/rides.csv', delimiter=','):
    users_df = pd.read_csv(users_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=users_df.shape
    ))
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=rides_df.shape
    ))
    completed_rides_df = rides_df[rides_df.state == 'completed']
    rides_df['daily_date'] = pd.to_datetime(rides_df['quote_date']).dt.normalize().astype(str)
    daily_rides_df = rides_df.groupby(['user_id', 'daily_date']).agg({'ride_id':'count', 'price_nominal':'sum'}).reset_index().rename(columns={'ride_id':'nb_rides', 'price_nominal':'total_price'})
    #Join the two dataframes
    joined_df = daily_rides_df.join(users_df.set_index('user_id'), on='user_id', how='inner')
    return joined_df


def create_chart_df(users_csv='raw_data/users.csv', rides_csv='raw_data/rides.csv', delimiter=','):
    users_df = clean_users_csv(users_csv, delimiter)
    rides_df = pd.read_csv(rides_csv, delimiter=delimiter)
    LOGGER.info(
        "Successfully read {shape} CSV (row(s), column(s)) into dataframe".format(
        shape=rides_df.shape
    ))
    joined_df = rides_df.join(users_df.set_index('user_id'), on='user_id', how='inner')
    joined_df['week_number'] = pd.to_datetime(joined_df['quote_date']).dt.week
    joined_df = joined_df[joined_df.state == "completed"].groupby(['week_number', 'loyalty_status', 'loyalty_status_txt']).agg({'ride_id':'count'}).reset_index().rename(columns={'ride_id':'nb_rides'})
    return joined_df

def plot_graph(df):
    df = df.pivot(index='week_number', columns='loyalty_status_txt', values='nb_rides')
    df.plot.bar()
    plt.show()
    