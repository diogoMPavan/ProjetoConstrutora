# Generated by Django 5.1.1 on 2024-09-29 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0015_alter_mov_financeira_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mov_financeira',
            name='Data',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 29, 17, 9, 37, 103862), verbose_name='Data'),
        ),
    ]
