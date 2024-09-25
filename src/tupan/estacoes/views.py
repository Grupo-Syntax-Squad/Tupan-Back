from .models import Estacao, Parametro, Endereco
from .serializers import EstacaoSerializer, EnderecoSerializer, ParametroSerializer
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
        serializer = EstacaoSerializer(data=request.body)
        if serializer.is_valid():
            serializer.save()
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
        serializer = EstacaoSerializer(estacao, data=request.body)
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
