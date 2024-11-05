from .models import Usuario
from usuarios.serializer import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes

class UsuariosView(APIView):
    def get_permissions(self):
        if self.request.method in ["POST", "GET"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    @extend_schema(
        description="Lista todos os usuários ativos",
        responses={200: UsuarioSerializer(many=True), 404: OpenApiResponse(description="Nenhum usuário cadastrado")}
    )
    def get(self, request):
        usuarios = Usuario.objects.all().filter(ativo=True)
        if not usuarios.exists():
            return Response({"mensagem": "Nenhum usuário cadastrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description="Cria um novo usuário",
        request=UsuarioSerializer,
        responses={201: UsuarioSerializer, 400: OpenApiResponse(description="Erro na requisição")}
    )
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosDetalhesView(APIView):
    def get_permissions(self):
        if self.request.method in ["POST", "GET"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    @extend_schema(
        description="Busca um usuário ativo pelo seu id",
        responses={
            302: OpenApiResponse(UsuarioSerializer),
            404: OpenApiResponse(description="Usuário não encontrado"),
            500: OpenApiResponse(description="Erro ao buscar usuário")
        }
    )
    def get(self, request, pk):
        try:
            usuario = Usuario.objects.all().filter(pk=pk).filter(ativo=True)
            serializer = UsuarioSerializer(usuario, many=True)
            if len(usuario) <= 0:
                return Response({"mensagem": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data[0], status=status.HTTP_302_FOUND)
        except Exception as e:
            return Response({"mensagem": f"Erro ao buscar usuário: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
            description="Inativa um usuário pelo seu id",
            responses={200: UsuarioSerializer, 404: OpenApiResponse(description="Usuário não encontrado"), 400: OpenApiResponse(description="Erro na requisição")}
    )
    def delete(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
            usuario.ativo = False
            usuario.save()
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Atualiza um usuário pelo seu id",
        request=UsuarioSerializer,
        responses={200: UsuarioSerializer, 404: OpenApiResponse(description="Usuário não encontrado"), 400: OpenApiResponse(description="Erro na requisição")}
    )
    def put(self, request, pk):
        try:
            new_data = request.data
            user = Usuario.objects.get(id=pk)
            user.email = new_data["email"]
            user.password = new_data["password"]
            user.save()
            serializer = UsuarioSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)