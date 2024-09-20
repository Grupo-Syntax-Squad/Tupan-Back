from .models import Usuario
from usuarios.serializer import UsuarioSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UsuarioList(APIView):
    """
    Lista, cria, atualiza e deleta os usuários.
    """
    def get(self, request, format=None):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        try:
            id_usuario = request.data.get("id")
            usuario = Usuario.objects.get(id=id_usuario)
            usuario.ativo = False
            usuario.save()
            return Response(usuario, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)