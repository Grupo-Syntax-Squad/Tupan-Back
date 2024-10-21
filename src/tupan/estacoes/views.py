from .models import Estacao, Parametro, Endereco
from .serializers import CategoriaSerializer, EstacaoSerializer, EnderecoSerializer, ParametroSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiRequest, OpenApiTypes

class EstacoesView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(EstacaoSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        ativo = request.query_params.get('ativo')
        estacoes = Estacao.objects.all()
        if (ativo):
            estacoes = estacoes.filter(ativo=ativo)   
        serializer = EstacaoSerializer(estacoes, many=True)
        return Response(serializer.data)
    
    @extend_schema(
            request=OpenApiRequest(EstacaoSerializer),
            responses={
                201: OpenApiResponse(EstacaoSerializer()),
                400: OpenApiResponse(description="Erro na requisição")
            }
    )
    def post(self, request, *args, **kwargs):
        try:
            endereco_instance = Endereco.objects.get(id=request.data["endereco"])
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        estacao_nome = request.data["nome"]
        if not estacao_nome:
            raise ValidationError("O nome da estação não pode ser vazio.")
        if Estacao.objects.filter(nome=estacao_nome).exists():
            raise ValidationError("Já existe uma estação com esse nome.")
        
        estacao = Estacao(nome=estacao_nome, endereco=endereco_instance, topico=request.data["topico"])
        estacao.save()

        parametros = request.data["parametros"]
        for p in parametros:
            parametro = Parametro.objects.get(id=p)
            estacao.parametros.add(parametro)

        serializer = EstacaoSerializer(estacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EstacoesDetalhesView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(EstacaoSerializer()),
            404: OpenApiResponse(description="Estação não encontrada")
        }
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EstacaoSerializer(estacao)
        return Response(serializer.data)
    
    @extend_schema(
        request=OpenApiRequest(EstacaoSerializer()),
        responses={
            200: OpenApiResponse(EstacaoSerializer()),
            400: OpenApiResponse(description="Erro na requisição"),
            404: OpenApiResponse(description="Estação não encontrada")
        }
            
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        parametros = request.data["parametros"]
        novosParametros = []
        for p in parametros:
            parametro = Parametro.objects.get(id=p)
            novosParametros.append(parametro)
        estacao.parametros.set(novosParametros)

        serializer = EstacaoSerializer(estacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses={
            204: OpenApiResponse(description="Estação deletada com sucesso"),
            404: OpenApiResponse(description="Estação não encontrada")
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            estacao = Estacao.objects.get(pk=pk)
        except Estacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        estacao.ativo = False
        estacao.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnderecosView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(EnderecoSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        enderecos = Endereco.objects.all()
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=OpenApiRequest(EnderecoSerializer),
        responses={
            201: OpenApiResponse(EnderecoSerializer()), 
            400: OpenApiResponse(description="Erro na requisição")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = EnderecoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnderecosDetalhesView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(EnderecoSerializer()), 
            404: OpenApiResponse(description="Endereço não encontrado")
        }
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)
    
    @extend_schema(
        request=OpenApiRequest(EnderecoSerializer),
        responses={
            200: OpenApiResponse(EnderecoSerializer()), 
            404: OpenApiResponse(description="Endereço não encontrado"), 
            400: OpenApiResponse(description="Erro na requisição")
        }
    )
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
    
    @extend_schema(
        responses={
            204: OpenApiResponse(description="Endereço deletado com sucesso"), 
            404: OpenApiResponse(description="Endereço não encontrado")
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            endereco = Endereco.objects.get(pk=pk)
        except Endereco.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        endereco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class ParametrosView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(ParametroSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        parametros = Parametro.objects.all()
        serializer = ParametroSerializer(parametros, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=OpenApiRequest(ParametroSerializer),
        responses={
            201: OpenApiResponse(ParametroSerializer()), 
            400: OpenApiResponse(description="Erro na requisição")
        }
    )
    def post (self, request, *args, **kwargs):
        serializer = ParametroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParametrosDetalhesView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(ParametroSerializer()), 
            404: OpenApiResponse(description="Parâmetro não encontrado")
        }
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(pk=pk)
        except Parametro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParametroSerializer(parametro)
        return Response(serializer.data)
    
    @extend_schema(
        request=OpenApiRequest(ParametroSerializer),
        responses={
            200: OpenApiResponse(ParametroSerializer()), 
            404: OpenApiResponse(description="Parâmetro não encontrado"), 
            400: OpenApiResponse(description="Erro na requisição")
        }
    )
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
    
    @extend_schema(
        responses={
            204: OpenApiResponse(description="Parâmetro deletado com sucesso"), 
            404: OpenApiResponse(description="Parâmetro não encontrado")
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(pk=pk)
        except Parametro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        parametro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriasView(APIView):
    @extend_schema(
            request=OpenApiRequest(CategoriaSerializer),
            responses={
                201: OpenApiResponse(CategoriaSerializer),
                400: OpenApiResponse(description="Erro ao cadastrar a categoria")
            }
    )
    def post (self, request, *args, **kwargs):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
