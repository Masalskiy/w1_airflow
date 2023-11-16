from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator

# аргументы дага по умолчанию
default_args = {
    "owner": "Denis Mas",
    # кол-во повторений при неуспешном выполнении
    "retries": 1, 
    # Если даг не отрработал, то через сколько повторить
    "retry_delay": timedelta(minutes=1), 
    # Дата, с которой начать выполнение дага
    "start_date": datetime(2023, 10, 12),
    # По какому пути находить файлы
    "template_searchpath" : "/tmp"
}

# Даг опреляется менеджером контекста
# Питоновский шаблон
with DAG(dag_id="01_bash_operator_example", 
         default_args=default_args, 
         description="bash operator example DAG",
         # до версии 2.4 нужно писать schedule
         schedule_interval="* * * * *",
         # для поиска среди других дагов (фишка версии 2.4)
         tags=["bash","Denis"], 
         # False говорит что не нужно запускать предыдущие задания. 
         # (в очередь не встанут задачи за пропущенные дни)
         catchup=False) as dag:
    # это какая-то точка входа для красоты
    start = EmptyOperator(task_id='start') 
    # важный параметр это task_id
    step = DummyOperator(task_id="step")

    
    bash = BashOperator(
        task_id='bash_operator_task',
        bash_command=f"echo 'Сейчас я создам папку:' && mkdir -p /tmp/test"
    )

    end = EmptyOperator(task_id='end')

    start >> step >> bash >> end

