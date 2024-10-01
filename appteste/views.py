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

        print('nome:' + nome)
        Usuario.objects.create(
            Nome = nome,
            Categoria_Usuario = categoria,
            Login = login,
            Senha = make_password(senha)
        )

        return redirect('../mostrarUsuarios/')


def mostrarUsuarios(request):
    obj_data = Usuario.objects.all()
    obj = Usuario.objects.all().select_related('Categoria_Usuario')
    template_name = "appteste/listaUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def deleteUsuario(request, f_id):
    usuario = Usuario.objects.get(id=f_id)
    if request.method == "POST":
        usuario.delete()
        return redirect('../mostrarUsuarios/')
    
def fazLogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        login = data.get('login')
        senha = data.get('senha')
        print('Login:' + login, 'senha' + senha)
        obj = Usuario.objects.all().values().filter(Login = login)
        if obj.Senha == make_password(senha):
            return render(request, template_name='appteste/home.html', context={"obj": obj})
        else:
            return render(request, template_name='appteste/login.html',context={"obj": obj})