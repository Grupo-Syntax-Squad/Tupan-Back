from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from usuarios.views import UsuariosView, UsuariosDetalhesView

urlpatterns = [
    path('usuarios', UsuariosView.as_view()),
    path('usuarios/<int:pk>', UsuariosDetalhesView.as_view())
]
