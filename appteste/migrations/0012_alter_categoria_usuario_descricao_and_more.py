# Generated by Django 5.1.1 on 2024-09-29 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0011_usuario_senha_alter_mov_financeira_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria_usuario',
            name='Descricao',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mov_financeira',
            name='Data',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 29, 1, 12, 55, 780762), verbose_name='Data'),
        ),
    ]
