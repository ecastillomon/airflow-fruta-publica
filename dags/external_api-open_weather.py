"""This dag only runs some simple tasks to test Airflow's task execution."""
import datetime as dt

import pendulum

from airflow.models.dag import DAG
from airflow.models import Variable
from airflow.decorators import task
import modules.function_etl as etl
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

now = pendulum.now(tz="UTC")
now_to_the_hour = (now - dt.timedelta(0, 0, 0, 0, 0, 3)).replace(minute=0, second=0, microsecond=0)
START_DATE = now_to_the_hour
DAG_NAME = 'external_api-open_weather'

#temp_c={'lat':19.3516286,'lon':-99.1777331}
main_loc=Variable.get("main_location")

api_key= Variable.get("api_key-open_weather")

fruit_db= Variable.get("fruit_db")

id_component='external_api-open_weather'

with  DAG(
    DAG_NAME,
    schedule_interval='* */2 * * *',
    default_args={'depends_on_past': False},
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    @task(task_id='get_forecast_weather')
    def get_open_weather_forecast():
        import requests
        import json
        import pandas as pd
        from airflow.providers.sqlite.hooks.sqlite import SqliteHook
        sqlite_hook=SqliteHook.get_hook(conn_id='sqlite-fp')
        url = "https://api.openweathermap.org/data/2.5/forecast"
        task_class='get_forecast_weather'
        temp_c=json.loads(main_loc)
        params = {'lat':temp_c['lat'],'lon':temp_c['lon'],'appid':api_key}

        response = requests.request("GET", url=url, params=params)
        print(response.text)
        response_json=response.json()
        res={'id_component':id_component, 'data':json.dumps(response_json),'date':format(dt.datetime.utcnow()),'class':task_class} 
        res=pd.DataFrame(res,index=[0])
        etl.write_df_table(res,'db_app_data',con=sqlite_hook.get_conn())     
    @task(task_id='get_current_weather')
    def get_open_weather():
        import requests
        import json
        import pandas as pd
        from airflow.providers.sqlite.hooks.sqlite import SqliteHook
        sqlite_hook=SqliteHook.get_hook(conn_id='sqlite-fp')
        #
        task_class='get_current_weather'
        url = "https://api.openweathermap.org/data/2.5/weather"
        temp_c=json.loads(main_loc)
        params = {'lat':temp_c['lat'],'lon':temp_c['lon'],'appid':api_key}
        response = requests.request("GET", url=url, params=params)
        print(response.text)  
        response_json=response.json()

        res={'id_component':id_component, 'data':json.dumps(response_json),'date':format(dt.datetime.utcnow()),'class':task_class} 
        res=pd.DataFrame(res,index=[0])
        etl.write_df_table(res,'db_app_data',con=sqlite_hook.get_conn())     
    get_forecast_task=get_open_weather_forecast()

    get_weather_task=get_open_weather()
    get_weather_task >> get_forecast_task

