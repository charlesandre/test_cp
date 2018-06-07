# Overview

__datawarehouse__ is a Python project to create a PostgreSQL database `cp_datawarehouse` and import  _Chauffeur Privé_ data inside.

The data sources for each table are located inside the `raw_data/` directory as CSV files.

The purpose of the following exercises is to assert many different technical skills. It is not essential to succeed in every question perfectly.


# _Chauffeur Privé_ Data Description

## Users Table
| column | definition |
| --- | ------- |
| `user_id` | *unique user id, primary key* |
| `loyalty_status` | *user loyalty status stored as integer: 0 = red, 1 = silver, 2 = gold, 3 = platinum* |
| `loyalty_status_txt` | *user loyalty status stored as text: red, silver, gold, platinum* |


## Rides Table
| column | definition |
| --- | ------- |
| `ride_id` | *unique ride id, primary key* |
| `user_id` | *user id* |
| `from_zipcode` | *zip code of the ride start location* |
| `to_zipcode` | *zip code of the ride end location* |
| `state` | *state of the ride: completed, not_completed: whether the ride was completed or not (for whatever possible reason)* |
| `quote_date` | *local date when the user sees the price of a ride in his app before ordering it* |
| `completed_date` | *local date when the ride is actually completed successfully* |
| `price_nominal` | *price of the ride* |
| `loyalty_points_earned` | *loyalty points awarded by the ride if elligible (=payed with real money, without discount or loyalty points). Only completed rides are eligibles.* |


# Requirements

- Python 3
- virtualenvwrapper
- docker
- docker-compose

# Setup

## Python3 virtualenv

[`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.org/en/latest/install.html) is a set 
of extensions to [`virtualenv`](https://virtualenvwrapper.readthedocs.io/en/latest/) for creating 
and deleting virtual environments and otherwise managing your development workflow.

Creating a virtualenv named e.g. `cp_dw` for the project:

```bash
$ pip install virtualenvwrapper
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv --python=`which python3` cp_dw
```

##### virtualenvwrapper basic commands

- list all virtualenv environments
```bash
$ lsvirtualenv -b
```

- Activate and deactivate environments
```bash
$ workon cp_dw
$ deactivate
```

- Remove environments
```bash
$ rmvirtualenv cp_dw
```

More commands in the [`documentation`](http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html).


## Install Python dependencies

```bash
$ cd datawarehouse/
$ workon cp_dw
$ pip install -r requirements.txt
```

## Install PostgreSQL Docker Container

[Install `docker-compose`](https://docs.docker.com/compose/install)


Create and start docker container with `PostgreSQL 9.5`:
```bash
$ docker-compose -f tests/tools/docker-compose.yml up -d
```

Check if the container is up:
```bash
$ docker-compose -f tests/tools/docker-compose.yml ps

      Name                    Command              State            Ports          
----------------------------------------------------------------------------------
tools_postgres_1   docker-entrypoint.sh postgres   Up      0.0.0.0:65432->5432/tcp 
```

## Run tests

Run Python tests with [pytest](https://docs.pytest.org/en/latest/) from inside the top `datawarehouse/` directory:
```bash
$ PYTHONPATH=. pytest
```

All tests should pass successfully:
```bash
======================================= test session starts ========================================
platform linux -- Python 3.5.2, pytest-3.6.1, py-1.5.3, pluggy-0.6.0
rootdir: datawarehouse, inifile:
collected 3 items                                                                                  

tests/config/test_config.py .                                                                [ 33%]
tests/etl/test_load.py .                                                                     [ 66%]
tests/etl/test_transform.py .                                                                [100%]

===================================== 3 passed in 0.35 seconds =====================================
```


# Exercises

## Data transform and load

1. Explore all files in the `datawarehouse/` project top directory and try to understand them.
2. Based on `raw_data/rides.csv` input values, write a Python function in `datawarehouse/etl/transform.py` to clean rides by keeping only the rides from the **_Île-de-France_** region.
3. Write a Python function to load data from a Pandas dataframe into the `cp_datawarehouse.rides` table.
4. Write tests for every function and run them with `pytest` to make sure they pass successfully.

## SQL

1. Create a table `cp_datawarehouse.users_daily_rides` with the following columns:
* user_id
* loyalty_status
* loyalty_status_txt
* daily_date: date of ride day
* nb_rides: number of completed rides made the user for the given day
* total_price: total ride price spent by the user for the given day
2. Write a SQL query listing the average basket per day. The average basket is the average completed ride price for a given period of time.
3. Write a SQL query listing the 5 days with the least number of completed rides.


## Pandas

1. From the `raw_data/*.csv` CSV files, answer the 3 previous questions using Python Pandas library.
2. Create a chart plotting the number of completed rides per week for each loyalty status.


## How to answer

1. In the `datawarehouse/` project directory, feel free to create or update all files/directories that you might think of.
2. Send us back your updated project as a zip archive or push it to GitHub, Bitbucket, etc. and send us the repository address.
