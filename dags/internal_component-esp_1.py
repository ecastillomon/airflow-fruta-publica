"""This dag only runs some simple tasks to test Airflow's task execution."""
import datetime as dt

import pendulum

from airflow.models.dag import DAG
from airflow.models import Variable
from airflow.decorators import task
import modules.function_etl as etl

now = pendulum.now(tz="UTC")
now_to_the_hour = (now - dt.timedelta(0, 0, 0, 0, 0, 3)).replace(minute=0, second=0, microsecond=0)
START_DATE = now_to_the_hour
DAG_NAME = 'internal_component-esp_1'

id_component='internal_component-esp_1'


fruit_db= Variable.get("fruit_db")
with  DAG(
    DAG_NAME,
    schedule_interval='*/1 * * * *',
    default_args={'depends_on_past': False},
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    @task(task_id='get_status')
    def get_status():
        import requests
        import json
        import pandas as pd
        from airflow.providers.sqlite.hooks.sqlite import SqliteHook
        sqlite_hook=SqliteHook.get_hook(conn_id='sqlite-fp')
        url = "http://192.168.1.169:8080/ping"
        task_class='get_status'
        status=False
        response = requests.request("GET", url=url)
        print(response.text)
    #response_json=response.json()
        res={'id_component':id_component, 'data':response.text,'date':format(dt.datetime.utcnow()),'class':task_class}   
        res=pd.DataFrame(res,index=[0])
        etl.write_df_table(res,'db_app_data',con=sqlite_hook.get_conn())     
    @task(task_id='get_humidity')
    def get_humidity():
        import requests
        import json
        import pandas as pd
        from airflow.providers.sqlite.hooks.sqlite import SqliteHook
        sqlite_hook=SqliteHook.get_hook(conn_id='sqlite-fp')
        url = "http://192.168.1.169:8080/get_humidity"
        task_class='get_humidity'
        response = requests.request("GET", url=url)
        print(response.text)
        response_json=response.json()
        res={'id_component':id_component, 'data':json.dumps(response_json),'date':format(dt.datetime.utcnow()),'class':task_class}            
        res=pd.DataFrame(res,index=[0])
        etl.write_df_table(res,'db_app_data',con=sqlite_hook.get_conn())             
    get_status_task=get_status()
    get_humidity_task=get_humidity()
    get_status_task >> get_humidity_task

