from django.db import models


class Base(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Categoria(Base):
    unidade = models.CharField(help_text="Unidade de medida do parâmetro", max_length=30, blank=False)
    nome = models.CharField(help_text="Nome da categoria do parâmetro", max_length=127, blank=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f"{self.nome} em {self.unidade}"


class Parametro(Base):
    nome = models.CharField(max_length=127)
    fator = models.DecimalField(default=1, max_digits=10, decimal_places=4,  help_text="Valor a ser multiplicado")
    offset = models.DecimalField(default=0, max_digits=10, decimal_places=4, help_text="Valor a ser adicionado")
    nome_json = models.CharField(help_text="Nome do campo no json", max_length=127)
    descricao = models.TextField(help_text="Descrição do que abrange o parâmetro", max_length=255, blank=True)
    categoria = models.ForeignKey(Categoria, help_text="Tipo do parametro e unidade", default=None, on_delete=models.CASCADE)

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
    complemento = models.CharField(max_length=127, blank=True, null=True)
    cep = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    longitude = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.cep


class Estacao(Base):
    nome = models.CharField(max_length=127, unique=True, null=False, blank=False)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, blank=False, null=False)
    topico = models.CharField(help_text="Tópico do broker MQTT", max_length=127)
    parametros = models.ManyToManyField(Parametro, blank=True, through='EstacaoParametro')

    class Meta:
        verbose_name = "Estação"
        verbose_name_plural = "Estações"

    def __str__(self):
        return self.nome


class EstacaoParametro(models.Model):
    estacao = models.ForeignKey(Estacao, on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    class Meta:
        db_table = "estacoes_estacao_parametro"
    
    def __str__(self):
        return f"{self.estacao.nome} - {self.parametro.nome}"
