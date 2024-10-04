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
    obj = Categoria_Usuario.objects.all().filter(Ativa = True)
    context = {"obj": obj}
    return render(request=request,
                  template_name='appteste/manutencaoUsuario.html', context=context)

def listaUsuario(request):
    obj = Usuario.objects.all().filter(Ativo = True)
    context = {"obj": obj}
    return render(request=request,
                  template_name='appteste/listaUsuario.html', context=context)

def listaEmpreendimento(request):
    return render(request=request,
                  template_name='appteste/listaEmpreendimento.html')

def listaCategorias(request):
    obj = Categoria_Usuario.objects.all().filter(Ativa = True)
    template_name = "appteste/manutencaoUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def salvaUsuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        categoria_id = request.POST.get('categoria')
        login = request.POST.get('login')
        senha = request.POST.get('senha')

        categoria = Categoria_Usuario.objects.get(id=categoria_id)

        Usuario.objects.create(
            Nome = nome,
            Categoria_Usuario = categoria,
            Login = login,
            Senha = make_password(senha)
        )
        usuarios = Usuario.objects.all()
        return redirect('listaUsuario')


def mostrarUsuarios(request):
    obj = Usuario.objects.all().select_related('Categoria_Usuario').filter(Ativo = True)
    template_name = "appteste/listaUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def deleteUsuario(request, f_id):
    usuario = Usuario.objects.get(id=f_id)
    if request.method == "POST":
        #usuario.delete()
        usuario.Ativo = False
        usuario.save()
        return redirect('listaUsuario')
    template_name = "appteste/confirmacao.html"
    context = {"usuario": usuario}
    return render(request, template_name, context)
    
def updateUsuario(request, f_id):
    usuario = Usuario.objects.select_related('Categoria_Usuario').get(id=f_id)
    if request.method == "POST":
       usuario = Usuario(request.POST, instance=usuario)
       usuario.save()
    template_name = "appteste/manutencaoUsuario.html"
    context = {"usuario": usuario}
    return render(request, template_name, context)

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