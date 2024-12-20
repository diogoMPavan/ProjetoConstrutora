from django.contrib import admin
from .models import Mov_Financeira
from .models import Categoria_Usuario
from .models import Categoria_Financeira
from .models import Usuario
from .models import Empreendimento
from tinymce.widgets import TinyMCE
from django.db import models

# Para o site de administração

class Categoria_UsuarioAdmin(admin.ModelAdmin):
    fields = ["Descricao", "Ativa"]

class Categoria_FinanceiraAdmin(admin.ModelAdmin):
    fields = ["Descricao", "Ativa"]

class Usuario_Admin(admin.ModelAdmin):
    fields = ["Nome",
              "Login",
              "Senha",
              "Ativo",
              "Categoria_Usuario"]
    
class Empreendimento_Admin(admin.ModelAdmin):
    fields = ["Nome",
              "Descricao",
              "Data_inicio",
              "Data_fim_prevista",
              "Data_fim",
              "UF",
              "Cidade",
              "Valor_total",
              "Ativo",
              "Usuario_id"]

class Mov_FinanceiraAdmin(admin.ModelAdmin):
    fields = ["A_pagar",
              "Descricao",
              "Valor",
              "Data",
              "Pendente",
              "Categoria_Financeira",
              "Empreendimento_id",
              "Usuario"]


admin.site.register(Categoria_Usuario, Categoria_UsuarioAdmin) 
admin.site.register(Categoria_Financeira, Categoria_FinanceiraAdmin) 
admin.site.register(Usuario, Usuario_Admin)
admin.site.register(Empreendimento, Empreendimento_Admin)
admin.site.register(Mov_Financeira, Mov_FinanceiraAdmin) 