from .models import Usuario
from usuarios.serializer import UsuarioSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes

class UsuarioList(APIView):
    """
    Lista, cria, atualiza e deleta os usuários.
    """
    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    @extend_schema(
        description="Lista todos os usuários ativos",
        responses={200: UsuarioSerializer(many=True), 404: OpenApiResponse(description="Nenhum usuário cadastrado")}
    )
    def get(self, request, format=None):
        usuarios = Usuario.objects.all().filter(ativo=True)
        if not usuarios.exists():
            return Response({"mensagem": "Nenhum usuário cadastrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    @extend_schema(
            description="Deleta um usuário pelo seu id",
            parameters=[
                OpenApiParameter("id", OpenApiTypes.INT, description="Id do usuário", required=True)
            ],
            responses={200: UsuarioSerializer, 404: OpenApiResponse(description="Usuário não encontrado"), 400: OpenApiResponse(description="Erro na requisição")}
    )
    def delete(self, request, format=None):
        try:
            id_usuario = request.data.get("id")
            usuario = Usuario.objects.get(id=id_usuario)
            usuario.ativo = False
            usuario.save()
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        description="Cria um novo usuário",
        request=UsuarioSerializer,
        responses={201: UsuarioSerializer, 400: OpenApiResponse(description="Erro na requisição")}
    )
    def post(self, request, format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza um usuário pelo seu id",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, description="Id do usuário", required=True)
        ],
        request=UsuarioSerializer,
        responses={200: UsuarioSerializer, 404: OpenApiResponse(description="Usuário não encontrado"), 400: OpenApiResponse(description="Erro na requisição")}
    )
    def put(self, request, id, format=None):
        try:
            new_data = request.data
            user = Usuario.objects.get(id)
            user.email = new_data["email"]
            user.password = new_data["password"]
            user.save()
            serializer = UsuarioSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)