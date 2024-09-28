from django.contrib import admin
from .models import Alerta, HistoricoAlerta, Medicao


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "condicao",
        "ativo",
        "criado",
        "modificado",
    ]
    list_filter = [
        "modificado",
        "criado",
        "ativo",
        "condicao",
    ]
    readonly_fields = [
        "criado",
        "modificado"
    ]


@admin.register(HistoricoAlerta)
class HistoricoAlertaAdmin(admin.ModelAdmin):
    list_display = [
        "alerta",
        "timestamp",
        "timestamp_convertido",
        "criado",
        "modificado",
    ]
    list_filter = [
        "alerta",
        "modificado",
        "criado",
        "timestamp_convertido",
    ]


@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = [
        "dados",
        "timestamp",
        "timestamp_convertido",
        "criado",
        "modificado",
    ]
    list_filter = [
        "modificado",
        "criado",
        "timestamp_convertido",
    ]
