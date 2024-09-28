from django.db import models
from datetime import datetime


class Base(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Alerta(Base):
    nome = models.CharField(help_text="Nome do alerta", max_length=127, unique=True)
    condicao = models.CharField(help_text="Condição para o alerta acontecer", max_length=4)
    ativo = models.BooleanField(default=True)
# falta a chave estrangeira da estacao_parametro

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

    def __str__(self):
        return self.nome


class HistoricoAlerta(Base):
    timestamp = models.BigIntegerField(help_text="Data/hora do alerta em timestamp" ,blank=False)
    alerta = models.ForeignKey(Alerta, related_name="historico_alertas", on_delete=models.CASCADE)
    timestamp_convertido = models.DateTimeField(help_text="Data/hora do alerta em datetime", blank=True, null=True)

    class Meta:
        verbose_name = "Histórico de Alerta"
        verbose_name_plural = "Históricos de Alertas"

    def save(self, *args, **kwargs):
        self.timestamp_convertido = datetime.fromtimestamp(self.timestamp)
        super(HistoricoAlerta, self).save(*args, **kwargs)


class Medicao(Base):
    timestamp = models.BigIntegerField(help_text="Data/hora da medição em timestamp", blank=False)
    timestamp_convertido = models.DateTimeField(help_text="Data/hora da medição em datetime", blank=True, null=True)
    dados = models.CharField(help_text="Valor dos dados da medição", max_length=63, blank=False, null=False)
# Falta a chave estrangeira estacao_parametro

    class Meta:
        verbose_name = "Medição"
        verbose_name_plural = "Medições"

    def save(self, *args, **kwargs):
        self.timestamp_convertido = datetime.fromtimestamp(self.timestamp)
        super(Medicao, self).save(*args, **kwargs)
