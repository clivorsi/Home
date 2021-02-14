import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import psycopg2 as db
import pandas as pd

def DBToJson():
    conn_string = "dbname='postgres' host='localhost' user='postgres' password='postgres'"
    conn=db.connect(conn_string)
    query="select * from heartdata"
    df = pd.read_sql(query,conn)
    print(len(df),'Rows',end='\n')
    json = df.to_json('./dagoutput/toAirflow.JSON',orient='records')
    print('JSON file printed',end='\n\n')
    
default_args = {
    'owner': 'craiglivorsi',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

dag = DAG(
    dag_id='db_to_json',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=dt.datetime(2021, 2, 13),
)


print_starting = BashOperator(
    task_id='starting',
    bash_command='echo "Reading DB data..."',
    dag=dag,
)

DBJson = PythonOperator(
    task_id='convertDBtoJson',
    python_callable=DBToJson,
    dag=dag,
)

print_starting >> DBJson          
