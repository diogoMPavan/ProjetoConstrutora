# Generated by Django 5.1.1 on 2024-09-29 03:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0006_usuario_mov_financeira_empreendimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mov_financeira',
            name='Data',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 29, 0, 54, 35, 608647), verbose_name='Data'),
        ),
    ]
