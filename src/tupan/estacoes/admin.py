from django.contrib import admin

from .models import Estacao, Parametro

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "fator",
        "offset",
        "unidade",
        "nome_json",
        "criado",
        "modificado",
    ]
    list_filter = [
        "modificado",
        "nome",
        "unidade",
        "criado"
    ]
    readonly_fields = [
        "criado",
        "modificado"
    ]

@admin.register(Estacao)
class EstacaoAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "endereco",
        "topico",
        "ativo",
        "parametros"
        "criado",
        "modificado",
    ]
    list_filter = [
        "modificado",
        "ativo",
        "nome",
        "criado"
    ]
    readonly_fields = [
        "criado",
        "modificado"
    ]
