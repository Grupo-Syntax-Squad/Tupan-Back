from django.urls import path
from .views import AlertasView, AlertasDetalhesView, HistoricoAlertaView, MedicaoView, MedicaoDetalhesView

urlpatterns = [
    path('alertas', AlertasView.as_view(), name='alertas'),
    path('alertas/<int:id>', AlertasDetalhesView.as_view(), name='alertas-detalhes'),
    path('historicos', HistoricoAlertaView.as_view(), name='historico-alertas'),
    path('medicoes', MedicaoView.as_view(), name='medicoes'),
    path('medicoes/<int:id>', MedicaoDetalhesView.as_view(), name='medicoes-detalhes')
]