# Test CP

## Requirements :
Virtualenv and docker as explained in the original readme. 
- Start the virtualenv
- Start the postgres docker container


## Data transform and load

2. The function is called clean_rides_csv inside cp_datawarehouse/etl/transform.py

3. The function is called insert_rides_list. 

4. Both test for this functions are located in test_transform.py and test_load.py inside tests/etl directory.


## SQL

The sql queries are located in the file requests.sql inside cp_datawarehouse/

## Pandas

1. The three functions are located in transform.py inside cp_datawarehouse/etl/. Tests are in test_transform.py
2. Composed of two functions located in transform.py :
      - First one is create_chart_df and return the dataframe formated for the graph (using pivot function). test located in test_transform.py
      - Second one plot the graph from a dataframe using matplotlib.


## How to run :

Enter your cp_dw virtualenv
```bash
# Start the Docker
$ docker-compose -f tests/tools/docker-compose.yml up -d

# Run the tests
$ PYTHONPATH=. pytest

#Run all the functions
$ PYTHONPATH=. python cp_datawarehouse/etl/run.py
```

-- Charles Andre --