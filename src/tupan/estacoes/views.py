from .models import Estacao, Parametro, Endereco
from .serializers import CategoriaSerializer, EstacaoSerializer, EnderecoSerializer, ParametroSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView




class EstacoesView(APIView):
    def get(self, request, *args, **kwargs):
        ativo = request.query_params.get('ativo')
        estacoes = Estacao.objects.all()
        if (ativo):
            estacoes = estacoes.filter(ativo=ativo)   
        serializer = EstacaoSerializer(estacoes, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):

        # Suponha que você tenha as instâncias já carregadas:
        endereco_instance = Endereco.objects.get(id=request.data["endereco"])

        # Criando uma nova Estacao
        estacao_nome = request.data["nome"]

        # Validando se o nome não está vazio
        if not estacao_nome:
            raise ValidationError("O nome da estação não pode ser vazio.")

        estacao = Estacao(nome=estacao_nome, endereco=endereco_instance, topico=request.data["topico"])

        # Antes de salvar, você pode verificar se a estação já existe
        if Estacao.objects.filter(nome=estacao.nome).exists():
            raise ValidationError("Já existe uma estação com esse nome.")

        # Salvar a estação
        estacao.save()

        # Adicionando parâmetros
        parametro_instance = Parametro.objects.get(id=request.data["parametros"])

        # Validando se o parâmetro existe
        if not parametro_instance:
            raise ValidationError("O parâmetro não existe.")

        estacao.parametros.add(parametro_instance)
        estacao.save()
        serializer = EstacaoSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EstacoesDetalhesView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EstacaoSerializer(estacao)
        return Response(serializer.data)
    def put(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EstacaoSerializer(estacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        estacao.ativo = False
        estacao.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnderecosView(APIView):
    def get(self, request, *args, **kwargs):
        enderecos = Endereco.objects.all()
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = EnderecoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnderecosDetalhesView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)
    def put(self, request, pk, *args, **kwargs):
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EnderecoSerializer(endereco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        endereco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class ParametrosView(APIView):
    def get(self, request, *args, **kwargs):
        parametros = Parametro.objects.all()
        serializer = ParametroSerializer(parametros, many=True)
        return Response(serializer.data)
    def post (self, request, *args, **kwargs):
        serializer = ParametroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParametrosDetalhesView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(pk=pk)
        except Parametro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParametroSerializer(parametro)
        return Response(serializer.data)
    def put(self, request, pk, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(pk=pk)
        except Parametro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParametroSerializer(parametro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(pk=pk)
        except Parametro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        parametro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriasView(APIView):
    def post (self, request, *args, **kwargs):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
