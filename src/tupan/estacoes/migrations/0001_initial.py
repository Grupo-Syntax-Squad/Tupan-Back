# Generated by Django 5.1.1 on 2024-10-08 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('unidade', models.CharField(help_text='Unidade de medida do parâmetro', max_length=30)),
                ('nome', models.CharField(help_text='Nome da categoria do parâmetro', max_length=127)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('logradouro', models.CharField(max_length=127)),
                ('bairro', models.CharField(max_length=127)),
                ('cidade', models.CharField(max_length=127)),
                ('estado', models.CharField(max_length=127)),
                ('numero', models.CharField(max_length=5)),
                ('complemento', models.CharField(max_length=127)),
                ('cep', models.CharField(max_length=8)),
                ('latitude', models.CharField(max_length=8)),
                ('longitude', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.CreateModel(
            name='Estacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=127)),
                ('topico', models.CharField(help_text='Tópico do broker MQTT', max_length=127)),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='estacoes.endereco')),
            ],
            options={
                'verbose_name': 'Estação',
                'verbose_name_plural': 'Estações',
            },
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=127)),
                ('fator', models.DecimalField(decimal_places=4, default=1, help_text='Valor a ser multiplicado', max_digits=10)),
                ('offset', models.DecimalField(decimal_places=4, default=0, help_text='Valor a ser adicionado', max_digits=10)),
                ('nome_json', models.CharField(help_text='Nome do campo no json', max_length=127)),
                ('descricao', models.TextField(blank=True, help_text='Descrição do que abrange o parâmetro', max_length=255)),
                ('categoria', models.ForeignKey(default=None, help_text='Tipo do parametro e unidade', on_delete=django.db.models.deletion.CASCADE, to='estacoes.categoria')),
            ],
            options={
                'verbose_name': 'Parâmetro',
                'verbose_name_plural': 'Parâmetros',
            },
        ),
        migrations.CreateModel(
            name='EstacaoParametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estacoes.estacao')),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estacoes.parametro')),
            ],
            options={
                'db_table': 'estacoes_estacao_parametros',
            },
        ),
        migrations.AddField(
            model_name='estacao',
            name='parametros',
            field=models.ManyToManyField(blank=True, through='estacoes.EstacaoParametro', to='estacoes.parametro'),
        ),
    ]
