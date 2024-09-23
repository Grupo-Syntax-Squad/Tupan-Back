from django.urls import path
from .views import estacao_list, estacao_details, parametro_list, parametro_details, endereco_list, endereco_details

urlpatterns = [
    path("estacoes", estacao_list, name="Estações"),
    path("estacoes/<int:pk>", estacao_details, name="Estação"),
    path("enderecos", endereco_list, name="Endereços"),
    path("enderecos/<int:pk>", endereco_details, name="Endereço"),
    path("parametros", parametro_list, name="Parâmetros"),
    path("parametros/<int:pk>", parametro_details, name="parâmetro")    
]