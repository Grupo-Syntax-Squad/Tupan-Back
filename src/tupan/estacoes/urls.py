from django.urls import path
from .views import EstacoesView

urlpatterns = [
    path("", EstacoesView.as_view(), name="Estações")
]