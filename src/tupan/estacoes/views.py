from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Estacao, Parametro

class EstacoesView(View):
    def get(sel, request, *args, **kwargs):
        estacoes = Estacao.objects.all().values()
        return JsonResponse(list(estacoes), safe=False)
    
