# Как это запускать?
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'


Добавил БД, в которой будет храниться 
raw_store - RAW (слой RAW)
core_store - CORE (cлой CORE)
dm_store - DATA MART (витрина данных)

примонтирована папка
/raw_data 


docker compose up airflow-init
docker compose up
