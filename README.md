# Base de conhecimento

## Ambiente

### Criar, ativar e instalar as dependencias doambiente virtual
```sh
python -m venv .venv
```
```sh
.\.venv\Scripts\activate
```
```sh
pip install -r .\requiments-dev.txt
```


## Testes

### Para rodar testes:
```sh
pytest
```
### Cobertura de testes
```sh
pytest --cov=tupan
```