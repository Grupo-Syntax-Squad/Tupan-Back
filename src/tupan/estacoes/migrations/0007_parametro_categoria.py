# Generated by Django 5.1.1 on 2024-10-01 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estacoes', '0006_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametro',
            name='categoria',
            field=models.ForeignKey(default=None, help_text='Tipo do parametro e unidade', on_delete=django.db.models.deletion.CASCADE, to='estacoes.categoria'),
        ),
    ]
