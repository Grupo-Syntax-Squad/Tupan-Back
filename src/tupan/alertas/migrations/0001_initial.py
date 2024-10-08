# Generated by Django 5.1.1 on 2024-09-12 01:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(help_text='nome do alerta', max_length=127, unique=True)),
                ('condicao', models.CharField(help_text='condição para o alerta acontecer', max_length=4)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Alerta',
                'verbose_name_plural': 'Alertas',
            },
        ),
        migrations.CreateModel(
            name='HistoricoAlerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('timestamp', models.BigIntegerField()),
                ('timestamp_convertido', models.DateTimeField(blank=True, null=True)),
                ('alerta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_alertas', to='alertas.alerta')),
            ],
            options={
                'verbose_name': 'Histórico de Alerta',
                'verbose_name_plural': 'Históricos de Alertas',
            },
        ),
    ]
