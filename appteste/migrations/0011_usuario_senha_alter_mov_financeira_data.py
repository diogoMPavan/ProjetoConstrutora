# Generated by Django 5.1.1 on 2024-09-29 04:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0010_usuario_mov_financeira_empreendimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='Senha',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mov_financeira',
            name='Data',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 29, 1, 5, 43, 126100), verbose_name='Data'),
        ),
    ]