import datetime as dt
from datetime import timedelta, date

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import psycopg2 as db
import pandas as pd
import yfinance as yf
import psycopg2 as db

def APIToDB():
    tickers = yf.Tickers('aapl')
    aapl = tickers.tickers.AAPL.history(period="max").reset_index()
    aapl['Stock Splits'] = aapl['Stock Splits'].astype('int')
    aapl = aapl[aapl.Date == date.today()]
    conn_string = "dbname='postgres' host='localhost' user='postgres' password='postgres'"
    conn=db.connect(conn_string)
    cur = conn.cursor()
    for row in aapl.values:
        cur.execute(
        "INSERT INTO aapl VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        row
        )
    conn.commit()
    
default_args = {
    'owner': 'craiglivorsi',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

dag = DAG(
    dag_id='api_to_db',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=dt.datetime(2021, 2, 13),
)

api_to_db = PythonOperator(
    task_id='api_to_db_py',
    python_callable=APIToDB,
    dag=dag,
)

api_to_db
