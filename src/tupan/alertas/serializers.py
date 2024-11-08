from rest_framework import serializers
from .models import Alerta, Medicao, HistoricoAlerta
from estacoes.serializers import EstacaoParametroSerializer, EstacaoSerializer

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields  = ('id', 'nome', 'condicao', 'estacao_parametro', 'criado', 'modificado', 'ativo')
        read_only_fields = ['estacao_parametro']

class MedicaoSerializer(serializers.ModelSerializer):
    estacao_parametro = EstacaoParametroSerializer()
    class Meta:
        model = Medicao
        fields = ('id', 'timestamp', 'timestamp_convertido', 'dados', 'estacao_parametro')

class HistoricoAlertaSerializer(serializers.ModelSerializer):
    estacao = EstacaoSerializer(source='alerta.estacao_parametro.estacao', read_only=True)

    class Meta:
        model = HistoricoAlerta
        fields = '__all__'