from rest_framework.views import APIView
from django.http import JsonResponse
import json
from .models import Alerta, HistoricoAlerta, Medicao


class AlertasView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            alertas = Alerta.objects.filter(ativo=True).values()
            return JsonResponse(list(alertas), safe=False)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            condicao = data.get('condicao')

            if not nome or not condicao:
                return JsonResponse({'error': 'Campos obrigatórios: nome, condicao'}, status=400)

            alerta = Alerta(nome=nome, condicao=condicao)
            alerta.save()

            return JsonResponse({
                'id': alerta.pk,
                'nome': alerta.nome,
                'condicao': alerta.condicao,
                'ativo': alerta.ativo
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)


class AlertasDetalhesView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            alerta = Alerta.objects.filter(id=id, ativo=True).values().first()
            if alerta:
                return JsonResponse(alerta, safe=False)
            else:
                return JsonResponse({'error': 'Alerta não encontrado ou inativo'}, status=404)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)

    def put(self, request, id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            alerta = Alerta.objects.filter(id=id, ativo=True).first()
            if alerta:
                alerta.nome = data.get('nome', alerta.nome)
                alerta.condicao = data.get('condicao', alerta.condicao)
                alerta.save()
                return JsonResponse({
                    'id': alerta.pk,
                    'nome': alerta.nome,
                    'condicao': alerta.condicao,
                    'ativo': alerta.ativo
                }, status=200)
            else:
                return JsonResponse({'error': 'Alerta não encontrado ou inativo'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
        except:
            return JsonResponse({'error': 'Erro ao atualizar alerta, tente novamente'}, status=500)

    def delete(self, request, id, *args, **kwargs):
        try:
            alerta = Alerta.objects.filter(id=id).first()
            if alerta:
                alerta.ativo = False
                alerta.save()
                return JsonResponse({'message': 'Alerta desativado com sucesso'}, status=200)
            else:
                return JsonResponse({'error': 'Alerta não encontrado'}, status=404)
        except:
            return JsonResponse({'error': 'Erro ao desativar alerta, tente novamente'}, status=500)


class HistoricoAlertaView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            historico = HistoricoAlerta.objects.get()
            return JsonResponse(list(historico), safe=False)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            timestamp = data.get('timestamp')
            alerta_id = data.get('alerta')

            if not timestamp or not alerta_id:
                return JsonResponse({'error': 'Campos obrigatórios: timestamp, alerta'}, status=400)

            alerta = Alerta.objects.get(pk=alerta_id)
            hist = HistoricoAlerta(timestamp=timestamp, alerta=alerta)
            hist.save()

            return JsonResponse({
                'id': hist.pk,
                'timestamp': hist.timestamp,
                'alerta': hist.alerta.pk,
                'timestamp_convertido': hist.timestamp_convertido
            }, status=201)
        except Alerta.DoesNotExist:
            return JsonResponse({'error': 'Alerta não encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erro ao salvar histórico: {str(e)}'}, status=500)


class MedicaoView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            medicoes = Medicao.objects.get()
            return JsonResponse(list(medicoes), safe=False)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)


class MedicaoDetalhesView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            alerta = Medicao.objects.filter(id=id, ativo=True).values().first()
            if alerta:
                return JsonResponse(alerta, safe=False)
            else:
                return JsonResponse({'error': 'Medição não encontrada ou inativa'}, status=404)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)
