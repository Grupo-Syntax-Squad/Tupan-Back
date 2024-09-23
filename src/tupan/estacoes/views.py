from .models import Estacao, Parametro, Endereco
from .serializers import EstacaoSerializer, EnderecoSerializer, ParametroSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def estacao_list(request):
    if request.method == 'GET':
        estacoes = Estacao.objects.all()
        serializer = EstacaoSerializer(estacoes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EstacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def estacao_details(request, pk):
    try:
        estacao = Estacao.objects.get(pk=pk)
    except Estacao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EstacaoSerializer(estacao)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EstacaoSerializer(estacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        estacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def endereco_list(request):
    if request.method == 'GET':
        enderecos = Endereco.objects.all()
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnderecoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def endereco_details(request, pk):
    try:
        endereco = Endereco.objects.get(pk=pk)
    except Endereco.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EnderecoSerializer(endereco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        endereco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def parametro_list(request):
    if request.method == 'GET':
        parametros = Parametro.objects.all()
        serializer = ParametroSerializer(parametros, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ParametroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def parametro_details(request, pk):
    try:
        parametro = Parametro.objects.get(pk=pk)
    except Parametro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParametroSerializer(parametro)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParametroSerializer(parametro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        parametro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



