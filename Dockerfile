FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos para o container
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Expôr a porta que o Django vai usar
EXPOSE 8000

# Comandos para rodar as migrações
CMD ["python", "src/tupan/manage.py", "makemigrations"]
CMD ["python", "src/tupan/manage.py", "migrate"]
# Comando para rodar o servidor
CMD ["python", "src/tupan/manage.py", "runserver", "0.0.0.0:8000"]

