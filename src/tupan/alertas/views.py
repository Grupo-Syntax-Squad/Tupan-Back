from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiRequest, OpenApiResponse
from django.http import JsonResponse
import json
from estacoes.models import EstacaoParametro
from .serializers import AlertaSerializer, MedicaoSerializer, HistoricoAlertaSerializer
from .models import Alerta, HistoricoAlerta, Medicao
from django.core.exceptions import ValidationError


class AlertasView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(AlertaSerializer(many=True)),
            400: OpenApiResponse(description="Parâmetro inválido para 'ativo'")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            # Obtém o valor do parâmetro 'ativo' da requisição, se disponível
            ativo_param = request.GET.get('ativo', None)

            if ativo_param is not None:
                ativo_param = ativo_param.strip().lower()
                if ativo_param == 'true':
                    ativo = True
                    alertas = Alerta.objects.filter(ativo=ativo).values()
                elif ativo_param == 'false':
                    ativo = False
                    alertas = Alerta.objects.filter(ativo=ativo).values()
                else:
                    raise ValidationError('Parâmetro inválido para "ativo".')
            else:
                alertas = Alerta.objects.all().values()

            return JsonResponse(list(alertas), safe=False)

        except ValidationError as ve:
                return JsonResponse({'error': str(ve)}, status=400)

        except Exception as e:
            return JsonResponse({
                'error': 'Erro ao buscar dados, tente novamente',
                'data': f"{e}"
            }, status=500)

    @extend_schema(
            request=OpenApiRequest(AlertaSerializer),
            responses={
                201: OpenApiResponse(AlertaSerializer),
                400: OpenApiResponse(description="Erro ao cadastrar um novo alerta")
            }
    )
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            condicao = data.get('condicao')
            ativo = data.get('ativo')

            parametro_estacao = data.get('estacao_parametro')
            estacao_parametro = EstacaoParametro.objects.get(estacao = parametro_estacao['estacao'], parametro = parametro_estacao['parametro'])
            if not nome or not condicao:
                return JsonResponse({'error': 'Campos obrigatórios: nome, condicao'}, status=400)

            alerta = Alerta(nome=nome, condicao=condicao, ativo=ativo, estacao_parametro=estacao_parametro)
            serializer = AlertaSerializer(alerta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)


class AlertasDetalhesView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(AlertaSerializer),
            404: OpenApiResponse(description="Alerta não encontrado ou inativo"),
            500: OpenApiResponse(description="Erro ao buscar dados, tente novamente")
        }
    )
    def get(self, request, id, *args, **kwargs):
        try:
            alerta = Alerta.objects.filter(id=id, ativo=True).values().first()
            if alerta:
                return JsonResponse(alerta, safe=False)
            else:
                return JsonResponse({'error': 'Alerta não encontrado ou inativo'}, status=404)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)

    @extend_schema(
        request=OpenApiRequest(AlertaSerializer),
        responses={
            200: OpenApiResponse(AlertaSerializer),
            400: OpenApiResponse(description="Erro ao atualizar o alerta"),
            404: OpenApiResponse(description="Alerta não encontrado ou inativo"),
            500: OpenApiResponse(description="Erro ao atualizar alerta, tente novamente")
        }
    )
    def put(self, request, id, *args, **kwargs):
        try:
            alerta = Alerta.objects.filter(id=id, ativo=True).first()
            if alerta:
                serializer = AlertaSerializer(alerta, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'error': 'Alerta não encontrado ou inativo'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
        except:
            return JsonResponse({'error': 'Erro ao atualizar alerta, tente novamente'}, status=500)

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Alerta desativado com sucesso"),
            404: OpenApiResponse(description="Alerta não encontrado"),
            500: OpenApiResponse(description="Erro ao desativar alerta")
        }     
    )
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
    @extend_schema(
        responses={
            200: OpenApiResponse(HistoricoAlertaSerializer(many=True)),
            500: OpenApiResponse("Erro ao buscar dados")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            historico = HistoricoAlerta.objects.get()
            return JsonResponse(list(historico), safe=False)
        except:
            return JsonResponse({'error': 'Erro ao buscar dados, tente novamente'}, status=500)

    @extend_schema(
        request=OpenApiRequest(HistoricoAlertaSerializer),
        responses={
            200: OpenApiResponse(HistoricoAlertaSerializer),
            400: OpenApiResponse(description="Campos obrigatórios: timestamp, alerta | Dados inválidos"),
            404: OpenApiResponse(description="Alerta não encontrado"),
            500: OpenApiResponse(description="Erro ao salvar histórico")
        }
    )
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
    @extend_schema(
        responses={
            302: OpenApiResponse(MedicaoSerializer(many=True)),
            404: OpenApiResponse(description="Nenhuma medição cadastrada"),
            500: OpenApiResponse(description="Erro ao buscar dados")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            medicoes = Medicao.objects.all()
            if not medicoes.exists():
                return Response({"mensagem": "Nenhuma medição cadastrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MedicaoSerializer(medicoes, many=True)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao buscar dados, tente novamente {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicaoDetalhesView(APIView):
    @extend_schema(
        responses={
            302: OpenApiResponse(MedicaoSerializer),
            404: OpenApiResponse(description="Nenhuma medição cadastrada"),
            500: OpenApiResponse(description="Erro ao buscar dados")
        }
    )
    def get(self, request, id, *args, **kwargs):
        try:
            medicao = Medicao.objects.get(pk=id)
            serializer = MedicaoSerializer(medicao)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Alerta.DoesNotExist:
            return Response({'error': 'Erro ao buscar dados, tente novamente'}, status=status.HTTP_404_NOT_FOUND)
