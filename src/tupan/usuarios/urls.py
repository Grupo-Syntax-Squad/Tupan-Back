from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from usuarios.views import UsuarioList

urlpatterns = [
    path('', UsuarioList.as_view())
]
