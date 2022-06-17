#!/bin/bash
source /home/leonarda/airflow-fruta-publica/venv/bin/activate
airflow initdb
airflow scheduler &
exec airflow webserver
