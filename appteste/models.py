from django.db import models
from datetime import datetime


#Aqui ficam as tabelas do banco, qualquer alteração nelas é feita aqui
#IMPORTANTE: após qualquer modificação aqui na model é necessário rodar os comandos:
# py manage.py makemigrations
# py manage.py migrate
#Eles irão salvar as alterações


class Categoria_Usuario(models.Model):
    Descricao = models.CharField(max_length=100)
    Ativa = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.Descricao

class Usuario(models.Model):
    Nome = models.CharField(max_length=200)
    Login = models.CharField(max_length=45)
    Senha = models.CharField(max_length=100)
    Ativo = models.BooleanField(default=True)
    Categoria_Usuario = models.ForeignKey(Categoria_Usuario, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.Login

class Categoria_Financeira(models.Model):
    Descricao = models.CharField(max_length=100)
    Ativa = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.Descricao

class Mov_Financeira(models.Model):
    A_pagar = models.BooleanField(default=False)
    Descricao = models.TextField(200)
    Valor = models.DecimalField(max_digits=10, decimal_places=2) 
    Data = models.DateTimeField("Data", default=datetime.now())
    Status = models.CharField(max_length=45)
    Meio_de_Transacao = models.CharField(max_length=45)
    Categoria_Financeira = models.ForeignKey(Categoria_Financeira, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Empreendimento(models.Model):
    Nome = models.CharField(max_length=100, default="")
    Descricao = models.TextField(max_length=200)
    Data_inicio = models.DateField("Data inicio", default=datetime.now)
    Data_fim_prevista = models.DateField("Data fim prev")
    Data_fim = models.DateField("Data fim")
    Cidade = models.CharField(max_length=50, default="")
    Valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    Ativo = models.BooleanField(default=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)