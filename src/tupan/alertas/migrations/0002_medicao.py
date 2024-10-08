# Generated by Django 5.1.1 on 2024-09-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('timestamp', models.BigIntegerField()),
                ('timestamp_convertido', models.DateTimeField(blank=True, null=True)),
                ('dados', models.CharField(max_length=63)),
            ],
            options={
                'verbose_name': 'Medição',
                'verbose_name_plural': 'Medições',
            },
        ),
    ]
