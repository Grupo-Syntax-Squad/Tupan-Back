from rest_framework import serializers
from .models import Alerta

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields  = ('id', 'nome', 'condicao', 'estacao_parametro', 'criado', 'modificado', 'ativo')
        read_only_fields = ['estacao_parametro']