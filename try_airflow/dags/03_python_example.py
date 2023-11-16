from datetime import datetime,timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

NAME = "Tommy"
AGE = 30

# аргументы дага по умолчанию
default_args = {
    "owner": "peter",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def greet(name, age):
    print(f"hello world! My name is {name}, and Im {age} old!")

with DAG(
    default_args = default_args,
    dag_id = '03_python_example',
    description = 'Пример DAG с PythonOperator',
    start_date = datetime(2023,10,12),
    schedule_interval = "*/1 * * * *",
    catchup=False

) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    task1 = PythonOperator(
        task_id='greet',
        python_callable = greet,
        op_kwargs = {'name':NAME, 'age': AGE}
    )


    start >> task1 >> end
