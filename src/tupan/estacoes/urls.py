from django.urls import path
from .views import EstacoesView, EstacoesDetalhesView, EnderecosView, EnderecosDetalhesView, ParametrosView, ParametrosDetalhesView

urlpatterns = [
    path("estacoes", EstacoesView.as_view(), name="Estações"),
    path("estacoes/<int:pk>", EstacoesDetalhesView.as_view(), name="Estação"),
    path("enderecos", EnderecosView.as_view(), name="Endereços"),
    path("enderecos/<int:pk>", EnderecosDetalhesView.as_view(), name="Endereço"),
    path("parametros", ParametrosView.as_view(), name="Parâmetros"),
    path("parametros/<int:pk>", ParametrosDetalhesView.as_view(), name="Parâmetro")    
]