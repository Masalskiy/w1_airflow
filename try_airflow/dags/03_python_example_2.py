from datetime import datetime,timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task

NAME = "Tommy"
AGE = 30

# аргументы дага по умолчанию
default_args = {
    "owner": "peter",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# def greet(name, age):
#     print(f"hello world! My name is {name}, and Im {age} old!")

with DAG(
    default_args = default_args,
    dag_id = '03_python_example_2',
    description = 'Пример DAG с PythonOperator',
    start_date = datetime(2023,10,12),
    schedule_interval = '@once'

) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    # task1 = PythonOperator(
    #     task_id='greet',
    #     python_callable = greet,
    #     op_kwargs = {'name':NAME, 'age': AGE}
    #)

    @task
    def greet(name, age):
        print(f"hello world! My name is {name}, and Im {age} old!")


    start >> greet("SUSANA",45) >> end
