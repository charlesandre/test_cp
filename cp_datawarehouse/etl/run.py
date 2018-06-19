#!/usr/bin/python

import csv
from load import (
    insert_users_list,
    insert_rides_list,
)
from transform import (
    get_average_basket,
    get_5_days_with_least_rides,
    create_users_daily_rides_df,
    create_chart_df,
    plot_graph,
    clean_users_csv
)

def load_data():
    with open('raw_data/users.csv') as csvfile:
        reader = clean_users_csv(csvfile)
        users_list = reader.values.tolist()
        insert_users_list(users_list)

    with open('raw_data/rides.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rides_list = list(reader)
        for i, r in enumerate(rides_list):
            rides_list[i] = [None if x == '' else x for x in r]
        insert_rides_list(rides_list)

def run_pandas_functions():
    #Add data from csv to database
    load_data()
    #Get average basket per day
    avg_basket = get_average_basket()
    print(avg_basket.head())
    #Get the 5 days with the least amount of rides. 
    days = get_5_days_with_least_rides()
    print(days)

    users_daily_rides_df = create_users_daily_rides_df()
    print(users_daily_rides_df.head())
    
    graph_df = create_chart_df()
    plot_graph(graph_df)

if __name__ == "__main__":
    run_pandas_functions()