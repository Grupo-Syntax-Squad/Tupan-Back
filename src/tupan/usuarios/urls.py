from django.urls import path
from usuarios.views import UsuariosView, UsuariosDetalhesView

urlpatterns = [
    path('usuarios', UsuariosView.as_view()),
    path('usuarios/<int:pk>', UsuariosDetalhesView.as_view())
]
