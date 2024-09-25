import pytest
import json
from django.urls import reverse
from .models import Alerta, HistoricoAlerta

@pytest.fixture
def alerta_auxiliar():
    alerta = {
        "nome": "Alerta1",
        "condicao": "<2",
    }
    return alerta


class TestAlerta:
    @pytest.mark.django_db
    def teste_criar_alerta(self, alerta_auxiliar):
        Alerta.objects.create(**alerta_auxiliar)

        assert Alerta.objects.count() == 1
        alerta_no_banco = Alerta.objects.first()

        assert alerta_no_banco.pk == 1
        assert alerta_no_banco.nome == alerta_auxiliar['nome']
        assert alerta_no_banco.condicao == alerta_auxiliar['condicao']
        assert alerta_no_banco.ativo == True

    @pytest.mark.django_db
    def teste_url_listar_alertas(self, client, alerta_auxiliar):
        Alerta.objects.create(**alerta_auxiliar)

        url = reverse("alertas")
        response = client.get(url)

        json_data = response.json()

        assert response.status_code == 200
        assert len(json_data) == 1
        assert json_data[0]['nome'] == "Alerta1"
        assert json_data[0]['condicao'] == "<2"

    @pytest.mark.django_db
    def teste_url_cadastrar_alerta(self, client, alerta_auxiliar):

        url = reverse("alertas")
        response = client.post(url, data=json.dumps(alerta_auxiliar), content_type="application/json")

        json_data = response.json()
        assert response.status_code == 201
        assert json_data['nome'] == 'Alerta1'
        assert json_data['ativo'] == True


class TestHistoricoAlerta:
    @pytest.fixture
    def historico_alerta_auxiliar(self, alerta_auxiliar):
        alerta = Alerta.objects.create(**alerta_auxiliar)
        hist = {
            "timestamp": 1726067292,
            "alerta": alerta
        }
        return hist

    @pytest.mark.django_db
    def teste_criar_historico(self, historico_alerta_auxiliar):
        HistoricoAlerta.objects.create(**historico_alerta_auxiliar)

        assert HistoricoAlerta.objects.count() == 1
        historico_no_banco = HistoricoAlerta.objects.first()

        assert historico_no_banco.pk == 1
        assert historico_no_banco.timestamp == historico_alerta_auxiliar['timestamp']
        assert historico_no_banco.alerta == historico_alerta_auxiliar['alerta']
