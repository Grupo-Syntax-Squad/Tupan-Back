from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'ativo', 'criacao', 'alterado')
    search_fields = ('email',)
    readonly_fields = ('criacao', 'alterado')
    ordering = ('email',)