# Generated by Django 5.1.1 on 2024-10-31 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0044_alter_mov_financeira_empreendimento_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mov_financeira',
            name='Empreendimento_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appteste.empreendimento'),
        ),
    ]
