import csv
from load import (
    insert_users_list,
    insert_rides_list,
)
from transform import (
    get_average_basket,
    get_least_number_5_days,
    create_users_daily_rides_df
)

def load_data():
    print("load data")
    with open('raw_data/users.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        users_list = list(reader)
        insert_users_list(users_list)

    with open('raw_data/rides.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rides_list = list(reader)
        for i, r in enumerate(rides_list):
            rides_list[i] = [None if x == '' else x for x in r]
        insert_rides_list(rides_list)

def run_pandas_functions():
    #get_average_basket()
    #get_least_number_5_days()
    create_users_daily_rides_df()

if __name__ == "__main__":
    run_pandas_functions()