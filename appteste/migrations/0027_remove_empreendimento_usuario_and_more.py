# Generated by Django 5.1.1 on 2024-10-20 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0026_empreendimento_uf_alter_mov_financeira_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empreendimento',
            name='Usuario',
        ),
        migrations.RemoveField(
            model_name='mov_financeira',
            name='Usuario',
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='Usuario_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mov_financeira',
            name='Usuario_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mov_financeira',
            name='Data',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 20, 16, 27, 54, 421051), verbose_name='Data'),
        ),
    ]