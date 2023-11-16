from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'start_date': datetime(2023, 1, 1),
    'owner': 'mdv',
    "retries": 1, 
    "retry_delay": timedelta(minutes=1), 
}

with DAG(
        dag_id='good_morning_1',
        default_args=default_args,
        description = 'dag_send_good_morning',
        tags=["bash","Denis"],
        # каждые 10 минут
        schedule_interval='10 * * * *',
        catchup=False) as dag:
    # точка входа для красоты
    start = EmptyOperator(task_id='start') 

    say_hello = BashOperator (
        task_id='say_hello',
        # bash_command='echo "Good morning my diggers!"',
        bash_command='docker info',
        dag=dag
    )


    get_cur_rate = DockerOperator (
        task_id = 'get_cur_rate',
        # image = 'masalskii/ex-rate',
        image = 'debian:buster-slim',
        docker_url = 'unix:///var/run/docker.sock',
        command ='echo "Hello world!"',
        network_mode = 'airflow',
        # mem_limit = '1gb',
        auto_remove=True,
        dag=dag
    )

    end = EmptyOperator(task_id='end') 

    start >> say_hello >> get_cur_rate >> end