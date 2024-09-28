from django.shortcuts import render
from django.http import HttpResponse
from appteste.models import Mov_Financeira

#aqui 'aponta' para determinada tela nos templates

def home(request):
    return render(request=request, 
                  template_name='appteste/home.html',
                  context={"Mov_financeira": Mov_Financeira.objects.all}) 

def login(request):
    return render(request=request,
                  template_name='appteste/login.html')