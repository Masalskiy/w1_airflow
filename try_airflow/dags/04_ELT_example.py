from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.hooks.postgres_hook import PostgresHook

import json
import requests

#***** Базовые константы ************

# соединение с базой person
conn_id = Variable.get("conn_name")


# Url Fake data
RANDOMUSER_URL_API= Variable.get("RANDOMUSER_URL_API")


def load_data_psql(**context):
    """Загружает cырые данные в PostgreSQL"""

    # соединяемся с БД
    hook = PostgresHook(postgres_conn_id=conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()

    try:
        # удалим сначала всё содержимое таблицы
        #cursor.execute(f"TRANCATE TABLE FROM person;")
        response = requests.get(RANDOMUSER_URL_API)
        data = response.json()

        name = data["results"][0]["name"]["first"]
        surname = data["results"][0]["name"]["last"]
        sex = data["results"][0]["gender"]
        age = data["results"][0]["dob"]["age"]
        country = data["results"][0]["location"]["country"]

        query = f"""

            INSERT INTO person_old (p_name,p_surname,sex,age,country) 
            VALUES ('{name}','{surname}','{sex}',{age},'{country}');



        """

        cursor.execute(query)
        conn.commit()

        cursor.close()
        conn.close()
        print("Данные успешно загружены в таблицу!")
        print("СТАТУС: ",context["task_instance"].current_state())
    except Exception as error:
        conn.rollback()
        raise Exception(f'Загрузить данные не получилось: {error}!')



# аргументы дага по умолчанию
default_args = {
    "owner": "peter",
    "retries": 5,
    "retry_delay": 5,
    "start_date": datetime(2023, 10, 11),
}

with DAG(dag_id="04_ELT_example", 
         default_args=default_args, 
         schedule_interval="*/60 * * * *", 
         description= "Пример ELT/ETL процесса", 
         template_searchpath = "/tmp", 
         catchup=False) as dag:

    start = EmptyOperator(task_id='start') 
    end = EmptyOperator(task_id='end')

    # загружаем в postgresql сырые данные
    load_datata_to_postgres = PythonOperator(
        task_id='load_data_to_psql',
        python_callable=load_data_psql
    )

    start >> load_datata_to_postgres >> end

