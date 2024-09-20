from django.contrib import admin

from .models import Endereco, Estacao, Parametro

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
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = [
        "logradouro",
        "numero",
        "bairro",
        "cep",
        "cidade",
        "estado",
        "complemento",
        "latitude",
        "longitude",
        "criado",
        "modificado",
    ]
    list_filter = [
        "cidade",
    ]
    readonly_fields = [
        "criado",
        "modificado"
    ]

@admin.register(Estacao)
class EstacaoAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "getEndereco",
        "topico",
        "getParametros",
        "ativo",
    ]
    list_filter = [
        "modificado",
        "nome",
        "criado"
    ]

    readonly_fields = [
        "criado",
        "modificado"
    ]

    def getParametros(self, obj):
        return ", ".join([parametro.nome for parametro in obj.parametros.all()])
    
    getParametros.short_description = 'Parâmetros'

    def getEndereco(self, obj):
        return obj.endereco.cep
    
    getEndereco.short_description = "Endereço"

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
