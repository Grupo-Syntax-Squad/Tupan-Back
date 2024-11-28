from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiRequest, OpenApiResponse, OpenApiParameter
from django.http import JsonResponse, HttpResponse
import csv
import json
from estacoes.models import EstacaoParametro
from .serializers import AlertaSerializer, MedicaoSerializer, HistoricoAlertaSerializer
from .models import Alerta, HistoricoAlerta, Medicao
from datetime import datetime
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
        parameters=[
            OpenApiParameter("timestamp_inicial", description="Timestamp inicial para filtragem", required=False, type=str),
            OpenApiParameter("timestamp_final", description="Timestamp final para filtragem", required=False, type=str),
            OpenApiParameter("timestamp", description="Timestamp para filtragem", required=False, type=str),
            OpenApiParameter("estacao_id", description="ID da estação para filtragem", required=False, type=int)
        ],
        responses={
            200: OpenApiResponse(HistoricoAlertaSerializer(many=True)),
            500: OpenApiResponse("Erro ao buscar dados")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            timestamp_inicial = request.query_params.get("timestamp_inicial")
            timestamp_final = request.query_params.get("timestamp_final")
            timestamp = request.query_params.get("timestamp")
            estacao_id = request.query_params.get("estacao_id")

            historico = HistoricoAlerta.objects.select_related('alerta__estacao_parametro__estacao').all()

            if timestamp_inicial and timestamp_final:
                historico = historico.filter(timestamp__range=[timestamp_inicial, timestamp_final])
            elif timestamp_inicial:
                historico = historico.filter(timestamp__gte=timestamp_inicial)
            elif timestamp_final:
                historico = historico.filter(timestamp__lte=timestamp_final)

            if timestamp:
                historico = historico.filter(timestamp=timestamp)

            if estacao_id:
                historico = historico.filter(alerta__estacao_parametro__estacao__id=estacao_id)

            serializer = HistoricoAlertaSerializer(historico, many=True)

            return JsonResponse(data=serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Erro ao buscar dados: {str(e)}'}, status=500)


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

class CSVHistoricoAlertasView(APIView):
    @extend_schema(
            parameters=[
                OpenApiParameter("data_inicio", description="Data inicial para filtragem no formato YYYY-MM-DD", required=False, type=str),
                OpenApiParameter("data_fim", description="Data final para filtragem no formato YYYY-MM-DD", required=False, type=str),
                OpenApiParameter("estacao_id", description="ID da estação para filtragem", required=False, type=int)
            ],
            responses={
                200: OpenApiResponse("Arquivo CSV gerado com sucesso"),
                500: OpenApiResponse("Erro ao buscar dados")
            }
        )
    def get(self, request):
        data_inicio = request.query_params.get('data_inicio')  # Formato esperado: 'YYYY-MM-DD'
        data_fim = request.query_params.get('data_fim')        # Formato esperado: 'YYYY-MM-DD'
        estacao_id = request.query_params.get('estacao_id')

        historico_alertas = HistoricoAlerta.objects.select_related('alerta', 'medicao', 'alerta__estacao_parametro__estacao')

        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                historico_alertas = historico_alertas.filter(timestamp_convertido__date__gte=data_inicio_dt)
            except ValueError:
                return HttpResponse("Formato inválido para 'data_inicio'. Use YYYY-MM-DD.", status=400)

        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                historico_alertas = historico_alertas.filter(timestamp_convertido__date__lte=data_fim_dt)
            except ValueError:
                return HttpResponse("Formato inválido para 'data_fim'. Use YYYY-MM-DD.", status=400)
        if estacao_id:
            historico_alertas = historico_alertas.filter(alerta__estacao_parametro__estacao__id=estacao_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="historico_alertas.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'ID',
            'Timestamp', 
            'Timestamp convertido', 
            'Nome do alerta', 
            'Condicao',
            'Nome da estacao',
            'ID da estacao',
            'Dados da Medicao'
        ])

        for alerta in historico_alertas.iterator():
            writer.writerow([
                alerta.id,
                alerta.timestamp,
                alerta.timestamp_convertido,
                alerta.alerta.nome,
                alerta.alerta.condicao,
                alerta.alerta.estacao_parametro.estacao.nome,
                alerta.alerta.estacao_parametro.estacao.id,
                alerta.medicao.dados if alerta.medicao else 'N/A'
            ])

        return response


class CSVMedicaoView(APIView):
    @extend_schema(
            parameters=[
                OpenApiParameter("data_inicio", description="Data inicial para filtragem no formato YYYY-MM-DD", required=False, type=str),
                OpenApiParameter("data_fim", description="Data final para filtragem no formato YYYY-MM-DD", required=False, type=str),
                OpenApiParameter("estacao_id", description="ID da estação para filtragem", required=False, type=int),
                OpenApiParameter("parametro_id", description="ID do parâmetro para filtragem", required=False, type=int)
            ],
            responses={
                200: OpenApiResponse("Arquivo CSV gerado com sucesso"),
                500: OpenApiResponse("Erro ao buscar dados")
            }
        )
    def get(self, request):
        data_inicio = request.query_params.get('data_inicio')  # Formato esperado: 'YYYY-MM-DD'
        data_fim = request.query_params.get('data_fim')        # Formato esperado: 'YYYY-MM-DD'
        estacao_id = request.query_params.get('estacao_id')
        parametro_id = request.query_params.get('parametro_id')

        medicoes = Medicao.objects.select_related('estacao_parametro__estacao')

        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                medicoes = medicoes.filter(timestamp_convertido__date__gte=data_inicio_dt)
            except ValueError:
                return HttpResponse("Formato inválido para 'data_inicio'. Use YYYY-MM-DD.", status=400)
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                medicoes = medicoes.filter(timestamp_convertido__date__lte=data_fim_dt)
            except ValueError:
                return HttpResponse("Formato inválido para 'data_fim'. Use YYYY-MM-DD.", status=400)
        if estacao_id:
            medicoes = medicoes.filter(estacao_parametro__estacao__id=estacao_id)
        if parametro_id:
            medicoes = medicoes.filter(estacao_parametro__parametro__id=parametro_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="medicoes.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'ID',
            'Timestamp',
            'Timestamp convertido',
            'Dados da medição',
            'Nome da estação',
            'ID da estação',
            'ID do parâmetro',
            'Nome do parâmetro'
        ])

        for medicao in medicoes.iterator():
            writer.writerow([
                medicao.id,
                medicao.timestamp,
                medicao.timestamp_convertido,
                medicao.dados,
                medicao.estacao_parametro.estacao.nome,
                medicao.estacao_parametro.estacao.id,
                medicao.estacao_parametro.parametro.id,
                medicao.estacao_parametro.parametro.nome,
            ])

        return response
