from rest_framework import serializers
from .models import Parametro, Endereco, Estacao

class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ('id', 'nome', 'fator', 'offset', 'unidade', 'nome_json', 'criado', 'modificado')

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'logradouro', 'bairro', 'cidade', 'estado', 'numero', 'complemento', 'cep', 'latitude', 'longitude', 'criado', 'modificado')

class EstacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacao
        fields = ('id', 'nome', 'endereco', 'topico', 'ativo', 'parametros', 'criado', 'modificado')
