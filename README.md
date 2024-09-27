# Base de conhecimento TUPAN-BACK

## Ambiente

### Criar, ativar e instalar as dependencias do ambiente virtual
```sh
python -m venv .venv
```
```sh
.\.venv\Scripts\activate
```
```sh
pip install -r .\requirements-dev.txt
```
### Varáveis de ambiente

Execute o seguinte comando para criar o .env
```bash
cp ./src/.env_sample ./src/.env
```
Logo em seguida altere as variáveis para os valores desejados.

## Swagger

### Gerando o schema para o swagger
Execute o seguinte comando no terminal para gerar o .yml que será utilizado pelo swagger:
```
python ./src/tupan/manage.py spectacular --color --file schema.yml
```

### Como acessar o swagger
Rode a aplicação e acesse o endpoint:
> /api/schema/swagger-ui

## Testes

### Para rodar testes:
```sh
pytest
```
### Cobertura de testes
```sh
pytest --cov=tupan
```