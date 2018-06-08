import csv
from load import (
    insert_users_list,
    insert_rides_list,
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

if __name__ == "__main__":
    load_data()