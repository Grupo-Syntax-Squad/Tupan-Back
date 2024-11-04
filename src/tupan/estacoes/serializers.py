from rest_framework import serializers
from .models import Categoria, Parametro, Endereco, Estacao, EstacaoParametro

class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ('id', 'nome', 'fator', 'offset', 'nome_json', 'descricao', 'categoria', 'criado', 'modificado')

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('id', 'logradouro', 'bairro', 'cidade', 'estado', 'numero', 'complemento', 'cep', 'latitude', 'longitude', 'criado', 'modificado')

class EstacaoSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    class Meta:
        model = Estacao
        fields = ('id', 'nome', 'endereco', 'topico', 'ativo', 'parametros', 'criado', 'modificado')

class EstacaoParametroSerializer(serializers.ModelSerializer):
    estacao = EstacaoSerializer()
    parametro = ParametroSerializer()
    class Meta:
        model = EstacaoParametro
        fields = ('id', 'estacao', 'parametro')

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields  = ('unidade', 'nome', 'criado', 'modificado', 'ativo')
