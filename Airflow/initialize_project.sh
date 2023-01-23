#!/bin/bash

sudo mkdir -p ./plugins/weather_app/data/testing/raw/
sudo chmod 777 ./plugins/weather_app/data/testing/raw/
sudo mkdir -p ./plugins/weather_app/data/testing/harmonized/
sudo chmod 777 ./plugins/weather_app/data/testing/harmonized/
sudo mkdir -p ./plugins/weather_app/data/testing/cleaned/
sudo chmod 777 ./plugins/weather_app/data/testing/cleaned/
sudo mkdir -p ./dags/
sudo chmod 777 ./dags/
sudo mkdir -p ./logs/
sudo chmod 777 ./logs/
sudo echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
sudo docker-compose up airflow-init
sudo docker-compose up