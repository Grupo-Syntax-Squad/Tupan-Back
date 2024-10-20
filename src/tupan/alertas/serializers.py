from rest_framework import serializers
from .models import Alerta, Medicao

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields  = ('id', 'nome', 'condicao', 'estacao_parametro', 'criado', 'modificado', 'ativo')
        read_only_fields = ['estacao_parametro']

class MedicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicao
        fields = ('id', 'timestamp', 'timestamp_convertido', 'dados', 'estacao_parametro')