from django.db import models
from datetime import datetime


#Aqui ficam as tabelas do banco, qualquer alteração nelas é feita aqui
#IMPORTANTE: após qualquer modificação aqui na model é necessário rodar os comandos:
# py manage.py makemigrations
# py manage.py migrate
#Eles irão salvar as alterações

class Mov_Financeira(models.Model):
    aPagar = models.BooleanField(default=False)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.DateTimeField("Data", default=datetime.now())
