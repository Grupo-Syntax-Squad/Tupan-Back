#!/bin/bash

# Aguarde o PostgreSQL estar pronto
echo "Aguardando o PostgreSQL estar pronto..."
while ! nc -z db 5432; do   
  sleep 0.1 # espera 1/10 de segundo
done
echo "PostgreSQL está pronto!"

# Rodar migrações
python src/tupan/manage.py makemigrations
python src/tupan/manage.py migrate  --noinput

# Iniciar o servidor
exec python src/tupan/manage.py runserver 0.0.0.0:8000