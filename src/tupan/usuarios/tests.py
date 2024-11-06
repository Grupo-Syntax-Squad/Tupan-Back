import json
import pytest
from .models import Usuario
from rest_framework.test import APIClient

class TestUsuario:
    @pytest.mark.django_db
    def test_criacao_usuarios(self):
        user1 = Usuario.objects.create_user(email='user@gmail.com', password='senha1')
        user2 = Usuario.objects.create_user(email='user2@gmail.com', password='senha2')

        assert Usuario.objects.count() == 2
        assert user1.email == 'user@gmail.com'
        assert user2.email == 'user2@gmail.com'

        assert user1.check_password("senha1")
        assert user2.check_password("senha2")

        assert user1.ativo == True
        assert user2.ativo == True

    @pytest.mark.django_db
    def test_listagem_usuarios(self):
        user1 = Usuario.objects.create_user(email='user@gmail.com', password='senha1')
        user2 = Usuario.objects.create_user(email='user2@gmail.com', password='senha2')

        usuarios = Usuario.objects.all()
        assert len(usuarios) == 2
        assert user1 in usuarios
        assert user2 in usuarios

    @pytest.mark.django_db
    def test_inativar_usuario(self):
        user = Usuario.objects.create_user(email="user@gmail.com", password="123123")
        user.ativo = False
        user.save()
        assert user.ativo == False

    @pytest.mark.django_db
    def test_atualizar_usuario(self, client):
        user = Usuario.objects.create_user(email="user@gmail.com", password="userpass")
        client = APIClient()
        client.force_authenticate(user=user)

        atualizacao = {
            "email": "test@gmail.com",
            "password": "userpass1"
        }
        url = f"/usuarios/{user.pk}"

        response = client.put(
            url,
            data=json.dumps(atualizacao),
            content_type="application/json"
        )
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["email"] == "test@gmail.com"