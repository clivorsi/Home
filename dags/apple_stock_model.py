import datetime as dt
from datetime import timedelta, date

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import psycopg2 as db
import pandas as pd
import yfinance as yf
import psycopg2 as db
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import joblib

def api_to_db():
    tickers = yf.Tickers('aapl')
    aapl = tickers.tickers.AAPL.history(period="5d").reset_index()
    aapl['Stock Splits'] = aapl['Stock Splits'].astype('int')
    aapl = aapl[aapl.Date.dt.strftime("%Y-%m-%d") == date.today().strftime("%Y-%m-%d")]
    conn_string = "dbname='postgres' host='localhost' user='postgres' password='postgres'"
    conn=db.connect(conn_string)
    cur = conn.cursor()
    for row in aapl.values:
        cur.execute(
        "INSERT INTO aapl VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        row
        )
    conn.commit()
    
def arima_model():
    conn_string = "dbname='postgres' host='localhost' user='postgres' password='postgres'"
    conn=db.connect(conn_string)
    query='select * from aapl'
    df = pd.read_sql(query,conn)
    df = df.set_index('date')
    df = pd.DataFrame(df.close)
    df_log = np.log(df)
    train_data = df_log[3:int(len(df_log)*0.9)]
    arima = ARIMA(train_data, order=(0, 1, 3))  
    model = arima.fit()
    filename = './clivorsi/models/diabetes_model.pkl'
    joblib.dump(model, filename)
    
default_args = {
    'owner': 'craiglivorsi',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

dag = DAG(
    dag_id='apple_stock_model',
    default_args=default_args,
    schedule_interval='30 21 * * *',
    start_date=dt.datetime(2021, 2, 17),
)

api_to_db = PythonOperator(
    task_id='api_to_db_py',
    python_callable=api_to_db,
    dag=dag,
)

create_arima_model = PythonOperator(
    task_id='arima_model_py',
    python_callable=arima_model,
    dag=dag,
)

api_to_db >> create_arima_model
