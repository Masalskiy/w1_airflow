import os
from pathlib import Path

from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

filename = Path(Variable.get("input_file"))


def check_file_at_path():
    """Проверяет наличие файла и создаёт ветвление"""

    file_path = Path(filename)
    if file_path.exists() == True:
        return "get_data"
    else:
        return "skip_file"

def read_file():
    """Функция чтения файла"""
    
    with open(filename, "r+") as f:
        for line in f.readlines():
            print(line)

# аргументы дага по умолчанию
default_args = {
    "owner": "peter",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "start_date": datetime(2023, 10, 12),
    "template_searchpath" : "/tmp"
}

with DAG(dag_id="06_branch_example", 
         default_args=default_args, 
         description="branch example DAG",
         schedule=None,
         tags=["branch","Peter"], 
         catchup=False) as dag:

    start = EmptyOperator(task_id='start') 

    skip_file = BashOperator(
        task_id='skip_file',
        bash_command=f"echo 'Файл не существует!'"
    )

    # проверяем есть ли файл по пути
    check_file_branch = BranchPythonOperator(
        task_id='check_file_at_path',
        python_callable=check_file_at_path
        
    )

    # Скачивает файл, если нет по пути
    get_data = PythonOperator(
        task_id='get_data',
        python_callable=read_file,
    )

    end = EmptyOperator(task_id='end', trigger_rule="none_failed")

    start >> check_file_branch >> [get_data, skip_file]
    [get_data, skip_file] >> end

