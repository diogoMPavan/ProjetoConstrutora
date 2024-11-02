from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from appteste.forms import RegisterUserForm
from appteste.models import Mov_Financeira
from .models import Categoria_Financeira
from .models import Categoria_Usuario, Usuario, Empreendimento
from django.contrib import messages
import base64
from datetime import datetime
from pyUFbr.baseuf import ufbr
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, logout, authenticate


#aqui 'aponta' para determinada tela nos templates

#============================== Abre telas ==================================
def home(request):
    if (request.user.is_authenticated):
        return render(request=request, template_name='home.html') 
    else:
        return redirect("login")

def login(request):
    return render(request=request,
                  template_name='registration/login.html')

def cadUsuario(request):
    if request.method == 'POST':
        group = request.user.groups
        print(group)
        if group == 'ADMIN':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuario criado com sucesso!")
                return redirect("listaUsuario")
        else:
            messages.error(request, "Seu usuário não tem permissão para criar um novo usuário")
            return redirect("listaUsuario")
    else:
        form = RegisterUserForm()
        context = {'form': form}
        return render(request=request, context=context, template_name='register.html')
    

def listaUsuario(request):
    usr = get_user_model()
    obj = usr.objects.all().filter(is_active=True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"usr": obj}
    if (request.user.is_authenticated):
        return render(request, template_name, context)
    else:
        return redirect('login')

def listaEmpreendimento(request):
    emp = Empreendimento.objects.all().filter(Ativo = True)
    mov_fin = Mov_Financeira.objects.filter(A_pagar = True)
    context = {"emp": emp, "mov_fin": mov_fin}
    return render(request=request, context=context,
                  template_name='appteste/Empreendimento/listaEmpreendimento.html')

def cadEmpreendimento(request):
    obj = Empreendimento.objects.all().filter(Ativo = True)
    context = {"obj": obj, "uf": ufbr.list_uf}
    if request.user.is_authenticated:
        return render(request=request, template_name='appteste/Empreendimento/manutencaoEmpreendimento.html', context=context) 
    else:
        return redirect('login')

def cadGastos(request, f_id):
    emp = Empreendimento.objects.get(id= f_id)
    cat = Categoria_Financeira.objects.all().filter(Ativa = True)
    context = {'empreendimentos': emp, 'categoria': cat}
    if request.user.is_authenticated:
        return render(request=request,context=context , template_name='appteste/Gastos/cadGastos.html')   
    else:
        return redirect('login')
#============================================================================
#========================== USUÁRIO ================================
def salvaUsuario(request):
   username = request.GET.get('username')
   password = request.GET.get('password')
   
   if User.objects.get(username=username, password=password) is None:
       user = User.objects.create(username, password)
       
   return redirect('listaUsuario')

def mostrarUsuarios(request):
    usr = get_user_model()
    obj = usr.objects.all().filter(is_active=True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"usr": obj}
    if (request.user.is_authenticated):
        return render(request, template_name, context)
    else:
        return redirect('login')

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
    usuario = User.objects.get(id=f_id)
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
        dataIni = datetime.strptime(dataIni, '%Y-%m-%d')
        dataIniFormatada = dataIni.strftime('%d/%m/%Y')
        dataFim = request.POST.get('dataFim')
        dataFim = datetime.strptime(dataFim, '%Y-%m-%d')
        dataFimFormatada = dataFim.strftime('%d/%m/%Y')
        uf = request.POST.get('uf') 
        cidade = request.POST.get('cidade')
        custo = request.POST.get('custo')
        ativo = request.POST.get('ativo')
        usuario = request.user

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
            Usuario_id = usuario
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
        dataIni = request.POST.get('dataInicio')
        dataIni = datetime.strptime(dataIni, '%Y-%m-%d')
        dataIniFormatada = dataIni.strftime('%d/%m/%Y')
        dataFim = request.POST.get('dataFim')
        dataFim = datetime.strptime(dataFim, '%Y-%m-%d')
        dataFimFormatada = dataFim.strftime('%d/%m/%Y')
        emp.Nome = request.POST.get('nome')
        emp.Descricao = request.POST.get('descricao')
        emp.Data_inicio = dataIni
        emp.Data_fim_prevista = dataFim
        emp.Data_fim = dataFim
        emp.UF = request.POST.get('uf')
        emp.Cidade = request.POST.get('cidade')
        emp.Valor_total = request.POST.get('custo')
        emp.Ativo = request.POST.get('ativo')
        emp.Usuario = request.user
        emp.save()
        return redirect('listaEmpreendimento')
    template_name = "appteste/Empreendimento/atualizaEmp.html"
    return render(request, template_name, {"emp": emp, "uf": ufbr.list_uf})

#============================================================================
#============================== CATEGORIA ===================================
def mostraCategoria(request):
    obj = Categoria_Financeira.objects.all().filter(Ativa = True)
    context = {"categorias": obj}
    if (request.user.is_authenticated):
        return render(request, template_name='appteste/CategoriaFinanceira/listaCategoria.html', context=context)
    else:
        return redirect('login')

def cadCategoria(request):
    if (request.method == 'POST'):
        Categoria_Financeira.objects.create(
            Nome = request.POST.get('nome'),
            Descricao = request.POST.get('descricao'),
            Ativa = True
        )
        return render(request, template_name='appteste/Empreendimento/listaEmpreendimento.html')
    else:
        return render(request, template_name='appteste/CategoriaFinanceira/cadCategoria.html')

#============================================================================
#========================== GASTOS ================================  
def salvaGastos(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        data = datetime.strptime(data, '%Y-%m-%d')
        dataIniFormatada = data.strftime('%d/%m/%Y')
        categoria = request.POST.get('categoria')
        cat_fin = Categoria_Financeira.objects.get(id=categoria)
        empreendimento = request.POST.get('emp')
        emp = Empreendimento.objects.get(id=empreendimento)
        
        Mov_Financeira.objects.create(
            A_pagar = True,
            Descricao = descricao,
            Valor = valor,
            Data = data,
            Pendente = True,
            Categoria_Financeira = cat_fin,
            Empreendimento_id = emp,
            Usuario = request.user
        )

        emp = Empreendimento.objects.get(id=empreendimento)
        emp.Valor_total += Decimal(valor)
        emp.save()

        return redirect('listaEmpreendimento')

def listaGastos(request):
    gastos = Mov_Financeira.objects.all().filter(A_pagar=True  ).order_by('Empreendimento_id')
    emp = Empreendimento.objects.all()
    context = {'gastos': gastos, 'emp':emp}
    if request.user.is_authenticated:
        return render(request, template_name='appteste/Gastos/listaGastos.html', context=context)
    else:
        return redirect('login')

def deleteGasto(request, f_id):
    gasto = Mov_Financeira.objects.get(id=f_id)
    emp = Empreendimento.objects.get(id=gasto.Empreendimento_id.id)
    if (request.method == 'POST'):
        gasto.delete()
        emp.Valor_total -= Decimal(gasto.Valor)
        emp.save()
        return redirect(listaEmpreendimento)
    else:
        template_name = "appteste/Gastos/confirmacaoGastos.html"
        context = {"gasto": gasto}
        return render(request, template_name=template_name, context=context)
    
def updateGasto(request, f_id):
    gasto = Mov_Financeira.objects.get(id=f_id)
    if (request.method == 'POST'):
        gasto.Descricao = request.POST.get('descricao')
        gasto.Valor = request.POST.get('valor')
        gasto.Data = request.POST.get('data')
        gasto.Categoria_Financeira = request.POST.get('categoria')
        gasto.Usuario = request.user
        gasto.save()
        return redirect('listaEmpreendimento')
    template_name = 'appteste/Gastos/atualizaGastos.html'
    emp = Empreendimento.objects.get(id=gasto.Empreendimento_id.id)
    cat = Categoria_Financeira.objects.all()
    context = {'gasto': gasto, 'empreendimentos': emp, 'cat': cat}
    return render(request, template_name, context=context)

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

def listaEmpreendimento(request):
    emp = Empreendimento.objects.all().filter(Ativo=True)
    paginator = Paginator(emp, 5)  # 5 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mov_fin = Mov_Financeira.objects.all().filter(A_pagar = True)

    context = {"emp": page_obj, "mov_fin": mov_fin}
    if request.user.is_authenticated:
        return render(request=request, context=context,
                  template_name='appteste/Empreendimento/listaEmpreendimento.html')
    else:
        return redirect('login')

def listaUsuario(request):
    usr = get_user_model()
    obj = usr.objects.all()
    paginator = Paginator(obj, 2)  # Define 2 usuários por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    context = {"emp": page_obj}
    return render(request=request, context=context,
                  template_name='appteste/Usuario/listaUsuario.html')

#================================================================