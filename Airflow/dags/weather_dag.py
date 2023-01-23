from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

# Import plugins.weather_app.source_to_raw as source_to_raw
from weather_app.source_to_raw.source_to_raw import get_raw_data_items
from weather_app.raw_to_harmonized.raw_to_harmonized import harmonize_data_files
from weather_app.harmonized_to_cleansed.harmonized_to_cleansed import data_file_cleaned
from weather_app.cleansed_to_sql.sql_functions import write_sql
from weather_app.geocode import get_multiple_locations


args = {'owner': 'ETL_weather_project',
    'start_date': days_ago(1)
}
dag = DAG(dag_id = 'weather_dag', default_args=args, schedule_interval='0 4 * * *')

with dag:
    
    get_raw_data_items = PythonOperator(
        task_id='get_raw_data_items',
        python_callable = get_raw_data_items
    )
    harmonize_data_files = PythonOperator(
        task_id='harmonize_data_files',
        python_callable = harmonize_data_files
    )
    clean_data_files = PythonOperator(
        task_id='clean_data_files',
        python_callable = data_file_cleaned
    )
    write_to_database = PythonOperator(
        task_id='write_to_database',
        python_callable = write_sql
    )
    get_locations = PythonOperator(
        task_id = 'get_locations',
        python_callable = get_multiple_locations
    )
    get_locations >> get_raw_data_items >> harmonize_data_files >> clean_data_files >> write_to_database