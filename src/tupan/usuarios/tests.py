import pytest
from .models import Usuario

class TestUsuario:

    @pytest.mark.django_db
    def test_criacao_usuarios(self):
        user1 = Usuario.objects.create_user(email='user@gmail.com', password='senha1')
        user2 = Usuario.objects.create_user(email='well@gmail.com', password='senha2')
        
        assert Usuario.objects.count() == 2
        assert user1.email == 'user@gmail.com'
        assert user2.email == 'well@gmail.com'
        
        assert user1.check_password("senha1")
        assert user2.check_password("senha2")

        assert user1.ativo == True
        assert user2.ativo == True

    @pytest.mark.django_db
    def test_listagem_usuarios(self):
        user1 = Usuario.objects.create_user(email='user@gmail.com', password='senha1')
        user2 = Usuario.objects.create_user(email='well@gmail.com', password='senha2')
        
        usuarios = Usuario.objects.all()
        assert len(usuarios) == 2
        assert user1 in usuarios
        assert user2 in usuarios