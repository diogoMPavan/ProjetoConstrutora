# Generated by Django 5.1.1 on 2024-09-29 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appteste', '0008_alter_mov_financeira_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mov_financeira',
            name='Categoria_Financeira',
        ),
        migrations.RemoveField(
            model_name='mov_financeira',
            name='Usuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='Categoria_Usuario',
        ),
        migrations.DeleteModel(
            name='Empreendimento',
        ),
        migrations.DeleteModel(
            name='Mov_Financeira',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
