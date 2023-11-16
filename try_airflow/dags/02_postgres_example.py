from datetime import datetime, timedelta, date

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="02_postgres_operator_example",
    start_date=datetime(2023, 10, 12),
    schedule="@once",
    catchup=False,
) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')
    
    create_person_table = PostgresOperator(
        task_id="create_person_table",
        postgres_conn_id="conn1",
        sql="sql/person_schema.sql",
    )

    populate_person_table = PostgresOperator(
        task_id="populate_person_table",
        postgres_conn_id="conn1",
        sql="sql/person_populate.sql",
    )

    start >> create_person_table >> populate_person_table >> end

    
