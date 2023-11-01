from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    # Когда первый раз будет запущен
    'start_date': datetime(2023, 1, 2),
    'owner': 'airflow'
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='My first DAG',
    # ежедневное выполнение
    schedule_interval='0 0 * * *' 
)

task1 = BashOperator(
    # task_id то как будем вызывать задание
    task_id='task1',
    bash_command='echo "Task 1"',
    dag=dag
)

task2 = BashOperator(
    task_id='task2',
    bash_command='echo "Task 2"',
    dag=dag
)

# Определение зависимости между задачами
task1 >> task2 