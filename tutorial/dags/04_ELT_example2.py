from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from airflow.hooks.postgres_hook import PostgresHook

import json
import requests

#***** Базовые константы ************

# соединение с базой person
conn_id = Variable.get("conn_name")


# Url Fake data
RANDOMUSER_URL_API= Variable.get("RANDOMUSER_URL_API")



def _extract_data():
    """Извлекаем данные из API"""

    try:
        response = requests.get(RANDOMUSER_URL_API)
        data = response.json()

        with open(f"/tmp/extract_data.sql", "w+") as f:
             
            name = data["results"][0]["name"]["first"]
            surname = data["results"][0]["name"]["last"]
            sex = data["results"][0]["gender"]
            age = data["results"][0]["dob"]["age"]
            country = data["results"][0]["location"]["country"]

            query = f"""

                INSERT INTO person_old (p_name,p_surname,sex,age,country) 
                VALUES ('{name}','{surname}','{sex}',{age},'{country}');

            """

            f.write(query)

    except Exception as error:
        raise Exception(f'Не удалось получить данные с API: {error}!')




# аргументы дага по умолчанию
default_args = {
    "owner": "peter",
    "retries": 5,
    "retry_delay": 5,
    "start_date": datetime(2023, 10, 11),
}

with DAG(dag_id="04_ELT_example2", 
         default_args=default_args, 
         schedule_interval="*/1 * * * *", 
         description= "Пример ELT/ETL процесса", 
         template_searchpath = "/tmp", 
         catchup=False) as dag:

    start = EmptyOperator(task_id='start') 
    end = EmptyOperator(task_id='end')

    extract_data = PythonOperator(
        task_id='exctract_data',
        python_callable=_extract_data
    )

    # выполнение sql-запросов на загрузку отзывов
    load_data = PostgresOperator(
        task_id=f"load_data",
        postgres_conn_id=conn_id,
        sql=f"extract_data.sql"
    )


    start >> extract_data >> load_data >> end

