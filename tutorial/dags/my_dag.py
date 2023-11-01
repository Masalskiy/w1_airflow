import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'start_date': datetime(2023, 1, 1),
    'owner': 'mdv'
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description = 'My first DAG',
    schedule_interval='0 0 * * *',
    catchup=False
)

task1 = BashOperator (
    task_id='task1',
    bash_command='echo "Hello world"',
    dag=dag
)

task2 = BashOperator(
    task_id='task2',
    sh_command='echo "Hello world  22"',
    dag=dag
)

task1 >> task2