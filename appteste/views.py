from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.hashers import make_password
from appteste.models import Mov_Financeira
from .models import Categoria_Financeira
from .models import Categoria_Usuario, Usuario

#aqui 'aponta' para determinada tela nos templates

def home(request):
    return render(request=request, 
                  template_name='appteste/home.html',
                  context={"Mov_financeira": Mov_Financeira.Categoria_Financeira}) 

def login(request):
    return render(request=request,
                  template_name='appteste/login.html')

def cadUsuario(request):
    return render(request=request,
                  template_name='appteste/manutencaoUsuario.html')

def listaUsuario(request):
    return render(request=request,
                  template_name='appteste/listaUsuario.html')

def listaEmpreendimento(request):
    return render(request=request,
                  template_name='appteste/listaEmpreendimento.html')

def listaCategorias(request):
    categorias = Categoria_Usuario.objects.all().values('id', 'Descricao').filter(Ativa = True)
    categorias_list = list(categorias)
    return JsonResponse(categorias_list, safe=False)

def salvaUsuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        categoria_id = data.get('categoria')
        login = data.get('login')
        senha = data.get('senha')
    
        categoria = Categoria_Usuario.objects.get(id=categoria_id)

        print(f"Login: {login}")
        Usuario.objects.create(
            Nome = nome,
            Categoria_Usuario = categoria,
            Login = login,
            Senha = make_password(senha)
        )

        return redirect('/')
    else:
        return redirect('../cadUsuario/')