"""This dag only runs some simple tasks to test Airflow's task execution."""
import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import os
now = pendulum.now(tz="UTC")
now_to_the_hour = (now - datetime.timedelta(0, 0, 0, 0, 0, 3)).replace(minute=0, second=0, microsecond=0)
START_DATE = now_to_the_hour
DAG_NAME = 'internal_component-awa'

fp_dir= Variable.get("fp_dir")
cargo_dir= Variable.get("cargo_dir")

awa_dir=os.path.join(fp_dir,'dags/lib/awa/Cargo.toml')

dag = DAG(
    DAG_NAME,
    schedule_interval='*/10 * * * *',
    default_args={'depends_on_past': False},
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)

t1 = BashOperator(task_id='internal_awa',bash_command=f'{cargo_dir} run --manifest-path {awa_dir}', dag=dag)
