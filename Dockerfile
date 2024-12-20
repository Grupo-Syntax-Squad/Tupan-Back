FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar netcat (openbsd)
RUN apt-get update && apt-get install -y netcat-openbsd

# Copiar o arquivo de requisitos para o container
COPY requirements.txt /app/
COPY entrypoint.sh /app/

# Instalar as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Criar um script de entrada
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expôr a porta que o Django vai usar
EXPOSE 8000

# Comando para rodar o script de entrada
CMD ["/app/entrypoint.sh"]

