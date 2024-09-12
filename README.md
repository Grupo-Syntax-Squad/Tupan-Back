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
pip install -r .\requiments-dev.txt
```
### Varáveis de ambiente

Execute o seguinte comando para criar o .env
```bash
cp ./src/.env_sample ./src/.env
```
Logo em seguida altere as variáveis para os valores desejados.


## Testes

### Para rodar testes:
```sh
pytest
```
### Cobertura de testes
```sh
pytest --cov=tupan
```