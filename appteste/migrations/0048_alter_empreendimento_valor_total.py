# Generated by Django 5.1.1 on 2024-11-03 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0047_categoria_financeira_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empreendimento',
            name='Valor_total',
            field=models.FloatField(),
        ),
    ]