from rest_framework import serializers
from usuarios.models import Usuario

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['user', 'email', 'ativo', 'criacao', 'alterado']