from django.db import models

from alertas.models import Base

class Parametro(Base):
    nome = models.CharField(max_length=127)
    fator = models.DecimalField(default=1, max_digits=10, decimal_places=4,  help_text="Valor a ser multiplicado")
    offset = models.DecimalField(default=0, max_digits=10, decimal_places=4, help_text="Valor a ser adicionado")
    unidade = models.CharField(max_length=30)
    nome_json = models.CharField(help_text="Nome do campo no json", max_length=127)

    class Meta:
        verbose_name = "Parâmetro"
        verbose_name_plural = "Parâmetros"
        
    def __str__(self):
        return self.nome

class Endereco(Base):
    logradouro = models.CharField(max_length=127)
    bairro = models.CharField(max_length=127)
    cidade = models.CharField(max_length=127)
    estado = models.CharField(max_length=127)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=127)
    cep = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    longitude = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.cep

class Estacao(Base):
    nome = models.CharField(max_length=127)
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.SET_NULL)
    topico = models.CharField(help_text="Tópico do broker MQTT", max_length=127)
    ativo = models.BooleanField(default=True)
    parametros = models.ManyToManyField(Parametro, blank=True)

    class Meta:
        verbose_name = "Estação"
        verbose_name_plural = "Estações"

    def __str__(self):
        return self.nome
    
