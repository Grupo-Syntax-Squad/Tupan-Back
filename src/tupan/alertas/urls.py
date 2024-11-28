from django.urls import path
from .views import (
    AlertasView,
    AlertasDetalhesView,
    HistoricoAlertaView,
    MedicaoView,
    MedicaoDetalhesView,
    CSVHistoricoAlertasView,
    CSVMedicaoView,
    )

urlpatterns = [
    path('alertas', AlertasView.as_view(), name='alertas'),
    path('alertas/<int:id>', AlertasDetalhesView.as_view(), name='alertas-detalhes'),
    path('historicos', HistoricoAlertaView.as_view(), name='historico-alertas'),
    path('medicoes', MedicaoView.as_view(), name='medicoes'),
    path('medicoes/<int:id>', MedicaoDetalhesView.as_view(), name='medicoes-detalhes'),
    path('historicos/csv', CSVHistoricoAlertasView.as_view(), name='historico-csv'),
    path('medicoes/csv', CSVMedicaoView.as_view(), name='medicoes-csv'),
]