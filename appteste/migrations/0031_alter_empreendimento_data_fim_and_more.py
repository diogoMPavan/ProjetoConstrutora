# Generated by Django 5.1.1 on 2024-10-20 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0030_alter_mov_financeira_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empreendimento',
            name='Data_fim',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='empreendimento',
            name='Data_fim_prevista',
            field=models.CharField(max_length=10),
        ),
    ]
