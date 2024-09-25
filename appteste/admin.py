from django.contrib import admin
from .models import Mov_Financeira
from tinymce.widgets import TinyMCE
from django.db import models

# Para o site de administração

class Mov_FinanceiraAdmin(admin.ModelAdmin):
    fields = ["valor",
              "tipo",
              "descricao",
              "date"]
    


admin.site.register(Mov_Financeira, Mov_FinanceiraAdmin) 