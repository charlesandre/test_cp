import csv
from load import (
    insert_users_list,
    insert_rides_list,
)

def load_data():
    print("load data")
    with open('raw_data/users.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        users_list = list(reader)
        insert_users_list(users_list)

if __name__ == "__main__":
    load_data()