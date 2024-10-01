# Generated by Django 5.1.1 on 2024-09-30 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0002_medicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerta',
            name='condicao',
            field=models.CharField(help_text='Condição para o alerta acontecer', max_length=4),
        ),
        migrations.AlterField(
            model_name='alerta',
            name='nome',
            field=models.CharField(help_text='Nome do alerta', max_length=127, unique=True),
        ),
        migrations.AlterField(
            model_name='historicoalerta',
            name='timestamp',
            field=models.BigIntegerField(help_text='Data/hora do alerta em timestamp'),
        ),
        migrations.AlterField(
            model_name='historicoalerta',
            name='timestamp_convertido',
            field=models.DateTimeField(blank=True, help_text='Data/hora do alerta em datetime', null=True),
        ),
        migrations.AlterField(
            model_name='medicao',
            name='dados',
            field=models.CharField(help_text='Valor dos dados da medição', max_length=63),
        ),
        migrations.AlterField(
            model_name='medicao',
            name='timestamp',
            field=models.BigIntegerField(help_text='Data/hora da medição em timestamp'),
        ),
        migrations.AlterField(
            model_name='medicao',
            name='timestamp_convertido',
            field=models.DateTimeField(blank=True, help_text='Data/hora da medição em datetime', null=True),
        ),
    ]
