# Generated by Django 5.1.1 on 2024-09-23 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
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
            name='Parametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=127)),
                ('fator', models.DecimalField(decimal_places=4, default=1, help_text='Valor a ser multiplicado', max_digits=10)),
                ('offset', models.DecimalField(decimal_places=4, default=0, help_text='Valor a ser adicionado', max_digits=10)),
                ('unidade', models.CharField(max_length=30)),
                ('nome_json', models.CharField(help_text='Nome do campo no json', max_length=127)),
            ],
            options={
                'verbose_name': 'Parâmetro',
                'verbose_name_plural': 'Parâmetros',
            },
        ),
        migrations.CreateModel(
            name='Estacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=127)),
                ('topico', models.CharField(help_text='Tópico do broker MQTT', max_length=127)),
                ('ativo', models.BooleanField(default=True)),
                ('endereco', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estacoes.endereco')),
                ('parametros', models.ManyToManyField(blank=True, to='estacoes.parametro')),
            ],
            options={
                'verbose_name': 'Estação',
                'verbose_name_plural': 'Estações',
            },
        ),
    ]
