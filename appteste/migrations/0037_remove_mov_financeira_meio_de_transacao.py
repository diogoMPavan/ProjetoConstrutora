# Generated by Django 5.1.1 on 2024-10-25 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0036_remove_mov_financeira_status_mov_financeira_pendente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mov_financeira',
            name='Meio_de_Transacao',
        ),
    ]
