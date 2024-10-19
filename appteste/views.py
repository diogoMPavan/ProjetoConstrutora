from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.hashers import make_password, check_password
#from django_cryptography.fields import encrypt, decrypt
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from appteste.models import Mov_Financeira
from .models import Categoria_Financeira
from .models import Categoria_Usuario, Usuario, Empreendimento
from django.contrib import messages
import base64
from pyUFbr.baseuf import ufbr

#aqui 'aponta' para determinada tela nos templates

#============================== Abre telas ==================================
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
                  template_name='appteste/Usuario/manutencaoUsuario.html', context=context)

def listaUsuario(request):
    obj = Usuario.objects.all().filter(Ativo = True)
    context = {"obj": obj}
    return render(request=request,
                  template_name='appteste/Usuario/listaUsuario.html', context=context)

def listaEmpreendimento(request):
    emp = Empreendimento.objects.all().filter(Ativo = True)
    context = {"emp": emp}
    return render(request=request, context=context,
                  template_name='appteste/Empreendimento/listaEmpreendimento.html')

def cadEmpreendimento(request):
    obj = Empreendimento.objects.all().filter(Ativo = True)
    context = {"obj": obj, "uf": ufbr.list_uf}
    return render(request=request, template_name='appteste/Empreendimento/manutencaoEmpreendimento.html', context=context)
#============================================================================

#========================== USUÁRIO ================================
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
            Senha = make_password(senha),
        )
        usuarios = Usuario.objects.all()
        return redirect('listaUsuario')

def mostrarUsuarios(request):
    obj = Usuario.objects.all().select_related('Categoria_Usuario').filter(Ativo = True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def deleteUsuario(request, f_id):
    usuario = Usuario.objects.get(id=f_id)
    if request.method == "POST":
        usuario.Ativo = False
        usuario.save()
        return redirect('listaUsuario')
    template_name = "appteste/Usuario/confirmacaoUsuario.html"
    context = {"usuario": usuario}
    return render(request, template_name, context)
    
def updateUsuario(request, f_id):
    usuario = Usuario.objects.select_related('Categoria_Usuario').get(id=f_id)
    obj = Categoria_Usuario.objects.all().filter(Ativa = True)
    if request.method == "POST":
       usuario.Nome = request.POST.get('nome')
       categoria = Categoria_Usuario.objects.get(id=request.POST.get('categoria'))
       usuario.Categoria_Usuario = categoria
       usuario.Login = request.POST.get('login')
       usuario.save()
       return redirect('listaUsuario')
    template_name = "appteste/Usuario/atualizaUsuario.html"
    return render(request, template_name, {"usuario": usuario, "obj": obj})
#============================================================================

#===================================== EMPREENDIMENTO =======================================
def salvaEmpreendimento(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        dataIni = request.POST.get('dataInicio')
        dataFim = request.POST.get('dataFim')
        uf = request.POST.get('uf') 
        cidade = request.POST.get('cidade')
        print("cidade: ", cidade)
        custo = request.POST.get('custo')
        ativo = request.POST.get('ativo')
        usuario = Usuario.objects.get(id=6)

        Empreendimento.objects.create(
            Nome = nome,
            Descricao = descricao,
            Data_inicio = dataIni,
            Data_fim_prevista = dataFim,
            Data_fim = dataFim,
            UF = uf,
            Cidade = cidade,
            Valor_total = custo,
            Ativo = ativo,
            Usuario = usuario
        )
        return redirect('listaEmpreendimento')
    
def deleteEmpreendimento(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    if request.method == "POST":
        emp.Ativo = False
        emp.save()
        return redirect('listaEmpreendimento')
    template_name = "appteste/Empreendimento/confirmacaoEmp.html"
    context = {"emp": emp}
    return render(request, template_name, context)

def updateEmpreendimento(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    if request.method == "POST":
        emp.Nome = request.POST.get('nome')
        emp.Descricao = request.POST.get('descricao')
        emp.Data_inicio = request.POST.get('dataInicio')
        emp.Data_fim_prevista = request.POST.get('dataFim')
        emp.Data_fim = request.POST.get('dataFim')
        emp.UF = request.POST.get('uf')
        emp.Cidade = request.POST.get('cidade')
        emp.Valor_total = request.POST.get('custo')
        emp.Ativo = request.POST.get('ativo')
        emp.Usuario = request.POST.get('usuario')
        emp.save()
        return redirect('listaEmpreendimento')
    template_name = "appteste/Empreendimento/atualizaEmp.html"
    return render(request, template_name, {"emp": emp, "uf": ufbr.list_uf})

#============================================================================

#=============================== GENÉRICAS =================================
def retornaCidades(request, uf):
    cidades = ufbr.list_cidades(uf)
    json_lst = json.dumps(cidades, ensure_ascii=False)
    return HttpResponse(json_lst)

def listaCategorias(request):
    obj = Categoria_Usuario.objects.all().filter(Ativa = True)
    template_name = "appteste/Usuario/manutencaoUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def fazLogin(request):
    if request.method == "POST":
        login = request.POST.get('login')
        senha = request.POST.get('senha')

        if verificaSenha(login, senha):
            messages.success(request, "Login realizado com sucesso")
            return render(request, template_name='appteste/home.html')
        else:
            messages.error(request, "Dados incorretos!")
            return render(request, template_name='appteste/login.html')
        
    for m in messages.get_messages(request):
            del m['senha']
            
def verificaSenha(login, senha):
    obj = Usuario.objects.all().filter(Login=login, Ativo=True)
    for o in obj:
        return check_password(senha, o.Senha)

#================================================================