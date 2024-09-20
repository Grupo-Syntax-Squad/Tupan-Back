from rest_framework import serializers
from usuarios.models import Usuario

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'password', 'ativo', 'criacao', 'alterado']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = Usuario.objects.create_user(**validated_data)
            return user