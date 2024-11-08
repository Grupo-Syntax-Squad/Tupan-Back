from django.contrib import admin

from .models import Endereco, Estacao, Parametro, Categoria, EstacaoParametro

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "fator",
        "offset",
        "nome_json",
        "criado",
        "modificado",
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


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        "unidade",
        "nome"
    ]
    list_filter = [
        "unidade"
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


class EstacaoParametroInline(admin.TabularInline):
    model = EstacaoParametro
    extra = 1

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

    inlines = [EstacaoParametroInline]

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
