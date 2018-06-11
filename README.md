# Test CP

## Requirements :
Virtualenv and docker as explained in the original readme. 
- Start the virtualenv
- Start the postgres docker container


## Data transform and load

2. The function is called clean_rides_csv inside cp_datawarehouse/etl/transform.py

3. The function is called insert_rides_list. 

4. Both test for this functions are located in test_transform.py and test_load.py inside tets/etl dir.

      You can run all those functions using this command : 
```bash
$ PYTHONPATH=. python cp_datawarehouse/etl/run.py
```

## SQL

The sql queries are located in the file requests.sql inside cp_datawarehouse/

## Pandas

1. The three functions are located in transform.py inside cp_datawarehouse/etl/. Test are in test_trasnform.py
2. Composed of two functions located in transform.py : 
      - First one is create_chart_df and return the dataframe formated for the graph (using pivot function). test in test_transform.py
      - Second is plot_graph and uses matplotlib.

-- Charles Andre -- 