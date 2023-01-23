## Instructions to run:

sudo echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

sudo docker-compose up airflow-init

sudo docker-compose up
