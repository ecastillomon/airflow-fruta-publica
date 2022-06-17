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
DAG_NAME = 'internal_component-webcam'


fruit_db= Variable.get("fruit_db")
with  DAG(
    DAG_NAME,
    schedule_interval='* */2 * * *',
    default_args={'depends_on_past': False},
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    @task(task_id='get_snapshot')
    def get_snapshot():
        import cv2
        
        cap = cv2.VideoCapture(0) 
        return_value, image = cap.read()
        cv2.imwrite('opencvtest1'+format(dt.datetime.now())+'.png', image)
        cap.release()      
    get_snaphot_task=get_snapshot()
