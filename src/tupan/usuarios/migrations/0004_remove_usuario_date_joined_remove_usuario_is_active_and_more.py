# Generated by Django 5.1.1 on 2024-09-20 11:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuario_date_joined_usuario_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_anonymous',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_authenticated',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_superuser',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='alterado',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='criacao',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at'),
        ),
    ]
