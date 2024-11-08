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
        "medicao",
        "timestamp",
        "timestamp_convertido",
        "criado",
    ]
    list_filter = [
        "alerta",
        "modificado",
        "criado",
    ]
    readonly_fields = [
        "criado",
        "timestamp_convertido",
        "modificado"
    ]


@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = [
        "dados",
        "timestamp",
        "estacao_parametro",
        "timestamp_convertido",
        "criado",
    ]
    list_filter = [
        "dados",
        "timestamp_convertido",
        "criado",
    ]
    readonly_fields = [
        "criado",
        "timestamp_convertido",
        "modificado"
    ]
