#!/bin/bash

# Rodar migrações
python src/tupan/manage.py makemigrations
python src/tupan/manage.py migrate

# Iniciar o servidor
python src/tupan/manage.py runserver 0.0.0.0:8000