import json
from multiprocessing.managers import BaseManager
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from appteste.forms import RegisterUserForm
from appteste.models import Mov_Financeira
from .models import Categoria_Financeira
from .models import Categoria_Usuario, Usuario, Empreendimento
from datetime import datetime
from pyUFbr.baseuf import ufbr
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import Empreendimento, Mov_Financeira, Categoria_Financeira, Usuario, Categoria_Usuario
from .forms import RegisterUserForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

#aqui 'aponta' para determinada tela nos templates
#============================== Abre telas ==================================

# Home
@login_required
def home(request):
    return render(request, 'home.html') 

def login(request):
    return render(request=request,
                  template_name='registration/login.html')
    
@login_required   
def listaUsuario(request):
    usr = get_user_model()
    obj = usr.objects.filter(is_active=True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"usr": obj}

    return render(request, template_name, context)

# Lista de Empreendimentos com busca
@login_required
def listaEmpreendimento(request):

    empreendimentos = Empreendimento.objects.filter(Ativo=True)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        uf = request.POST.get('uf')
        cidade = request.POST.get('cidade')

        if nome:
            empreendimentos = empreendimentos.filter(Nome=nome)
        if descricao:
            empreendimentos = empreendimentos.filter(Descricao__icontains=descricao)
        if uf:
            empreendimentos = empreendimentos.filter(UF__icontains=uf)
        if cidade:
            empreendimentos = empreendimentos.filter(Cidade__icontains=cidade)

    paginator = Paginator(empreendimentos, 5)
    page_number = request.GET.get('page')
    empreendimentos = paginator.get_page(page_number)

    mov_fin = Mov_Financeira.objects.filter(A_pagar=True)

    context = {
        "emp": empreendimentos,
        "mov_fin": mov_fin,
    }
    
    return render(request, 'appteste/Empreendimento/listaEmpreendimento.html', context)

# Cadastro de Empreendimento
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/listaEmpreendimento/')
def cadEmpreendimento(request):
    obj = Empreendimento.objects.filter(Ativo=True)
    context = {"obj": obj, "uf": ufbr.list_uf}

    return render(request, 'appteste/Empreendimento/manutencaoEmpreendimento.html', context) 
 
# Cadastro de Gastos
@login_required
def cadGastos(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    cat = Categoria_Financeira.objects.filter(Ativa=True)
    context = {'empreendimentos': emp, 'categoria': cat}
    

    return render(request, 'appteste/Gastos/cadGastos.html', context)

#============================================================================

#========================== USUÁRIO ================================
@login_required
def register(request):  
    if request.method == 'POST':  
        form = RegisterUserForm(request.POST)  
        if form.is_valid(): 
            tst = User.objects.filter(username
                                      =form.data.get('username'))
            if (form.data.get('password1') == form.data.get('password2') and tst.exists() == False):
                User.objects.create_user(username=form.data.get('username'),email=form.data.get('email') ,
                                     password=form.data.get('password1'), is_staff=True)
                user = User.objects.get(username=form.data.get('username'))
                grupo = Group.objects.get(name = 'PADRAO')
                user.groups.add(grupo)
                return redirect('home') 
            else:
                return render(request, 'register.html', {'form': form}) 
        else:
            return render(request, 'register.html', {'form': form})    
    else:
        form = RegisterUserForm()
        return render(request, 'register.html', {'form': form})

# Exibe a lista de usuários ativos
def mostrarUsuarios(request):
    usr = get_user_model()
    obj = usr.objects.filter(is_active=True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"usr": obj}
    
    if request.user.is_authenticated:
        return render(request, template_name, context)
    else:
        return redirect('login')

# Deleta usuário
@user_passes_test(lambda u: u.is_superuser, login_url='/mostrarUsuarios/')
def deleteUsuario(request, f_id):
    usuario = User.objects.get(id=f_id)
    if request.method == "POST":
        usuario.is_active = False
        usuario.save()
        return redirect('listaUsuario')
    
    template_name = "appteste/Usuario/confirmacaoUsuario.html"
    context = {"usuario": usuario}
    return render(request, template_name, context)
    
# Atualiza os dados do usuário
@user_passes_test(lambda u: u.is_superuser, login_url='/mostrarUsuarios/')
def updateUsuario(request, f_id):
    usuario = User.objects.get(id=f_id)
    if request.method == "POST":
       form = UpdateUserForm(request.POST)
       if form.is_valid():
          usuario.username = form.data.get('username')
          usuario.email = form.data.get('email')
          usuario.save()
          return redirect("listaUsuario")
    template_name = "appteste/Usuario/updateUser.html"
    form = UpdateUserForm()
    return render(request, template_name, {"usuario": usuario, "form": form})

#============================================================================

#===================================== EMPREENDIMENTO =======================================

# Salva um novo empreendimento
@user_passes_test(lambda u: u.is_superuser, login_url='/listaEmpreendimento/')
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
        custo = float(request.POST.get('custo'))
        ativo = request.POST.get('ativo')
        usuario = request.user.id

        Empreendimento.objects.create(
            Nome=nome,
            Descricao=descricao,
            Data_inicio=dataIni,
            Data_fim_prevista=dataFim,
            Data_fim=dataFim,
            UF=uf,
            Cidade=cidade,
            Valor_total=custo,
            Ativo=ativo,
            Usuario_id=usuario
        )
        return redirect('listaEmpreendimento')

# Deleta empreendimento
@user_passes_test(lambda u: u.is_superuser, login_url='/listaEmpreendimento/')
def deleteEmpreendimento(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    if request.method == "POST":
        emp.Ativo = False
        emp.save()
        return redirect('listaEmpreendimento')
    
    template_name = "appteste/Empreendimento/confirmacaoEmp.html"
    context = {"emp": emp}
    return render(request, template_name, context)

# Atualiza empreendimento
@user_passes_test(lambda u: u.is_superuser, login_url='/listaEmpreendimento/')
def updateEmpreendimento(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    if request.method == "POST":
        dataIni = request.POST.get('dataInicio')
        dataIni = datetime.strptime(dataIni, '%Y-%m-%d')
        dataFim = request.POST.get('dataFim')
        dataFim = datetime.strptime(dataFim, '%Y-%m-%d')
        emp.Nome = request.POST.get('nome')
        emp.Descricao = request.POST.get('descricao')
        emp.Data_inicio = dataIni
        emp.Data_fim_prevista = dataFim
        emp.Data_fim = dataFim
        emp.UF = request.POST.get('uf')
        emp.Cidade = request.POST.get('cidade')
        emp.Valor_total = request.POST.get('custo')
        emp.Ativo = request.POST.get('ativo')
        emp.Usuario = request.user.id
        emp.save()
        return redirect('listaEmpreendimento')
    
    template_name = "appteste/Empreendimento/atualizaEmp.html"
    return render(request, template_name, {"emp": emp, "uf": ufbr.list_uf})

#============================================================================

#============================== CATEGORIA ===================================

# Exibe as categorias financeiras
def mostraCategoria(request):
    obj = Categoria_Financeira.objects.filter(Ativa=True)
    context = {"categorias": obj}
    
    if request.user.is_authenticated:
        return render(request, template_name='appteste/CategoriaFinanceira/listaCategoria.html', context=context)
    else:
        return redirect('login')

# Cadastro de categoria financeira
def cadCategoria(request):
    if request.method == 'POST':
        Categoria_Financeira.objects.create(
            Nome=request.POST.get('nome'),
            Descricao=request.POST.get('observacao'),
            Ativa=True
        )
        return redirect('listaEmpreendimento')
    else:
        return render(request, template_name='appteste/CategoriaFinanceira/cadCategoria.html')

#============================================================================

#========================== GASTOS ================================

# Salva um novo gasto
def salvaGastos(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        data = datetime.strptime(data, '%Y-%m-%d')
        categoria = request.POST.get('categoria')
        cat_fin = Categoria_Financeira.objects.get(id=categoria)
        empreendimento = request.POST.get('emp')
        emp = Empreendimento.objects.get(id=empreendimento)
        
        Mov_Financeira.objects.create(
            A_pagar=True,
            Descricao=descricao,
            Valor=valor,
            Data=data,
            Pendente=True,
            Categoria_Financeira=cat_fin,
            Empreendimento_id=emp,
            Usuario=request.user
        )

        emp.Valor_total += float(valor)
        emp.save()

        return redirect('listaEmpreendimento')

# Exibe os gastos
@login_required
def listaGastos(request):
    if (request.method == 'POST'):
        categoria = request.POST.get('categoria')
        data1 = request.POST.get('data1')
        if data1:
            data1 = datetime.strptime(data1, '%Y-%m-%d')
        data2 = request.POST.get('data2')
        if data2:
            data2 = datetime.strptime(data2, '%Y-%m-%d')
        empreendimento = request.POST.get('empreendimento')
        gastos = Mov_Financeira.objects.filter(A_pagar = True)
        if (categoria != ""):
            gastos = gastos.filter(Categoria_Financeira = categoria)
        if (data1 != "" or data2 != ""):
            gastos = gastos.filter(Data__gte=data1, Data__lte=data2)
        if (empreendimento != ""):
            gastos = gastos.filter(Empreendimento_id = empreendimento)
    else:
        gastos = Mov_Financeira.objects.filter(A_pagar=True).order_by('Empreendimento_id')

    emp = Empreendimento.objects.filter(Ativo=True)
    categorias = Categoria_Financeira.objects.filter(Ativa=True)
    context = {'gastos': gastos, 'emp': emp, 'categorias': categorias}
    
    return render(request, 'appteste/Gastos/listaGastos.html', context)

# Deleta gasto
def deleteGasto(request, f_id):
    gasto = Mov_Financeira.objects.get(id=f_id)
    emp = Empreendimento.objects.get(id=gasto.Empreendimento_id.id)
    if request.method == 'POST':
        gasto.delete()
        emp.Valor_total -= float(gasto.Valor)
        emp.save()
        return redirect('listaEmpreendimento')
    
    template_name = "appteste/Gastos/confirmacaoGastos.html"
    context = {"gasto": gasto}
    return render(request, template_name, context)

# Atualiza gasto
def updateGasto(request, f_id):
    gasto = Mov_Financeira.objects.get(id=f_id)
    if request.method == 'POST':
        gasto.Descricao = request.POST.get('descricao')
        gasto.Valor = request.POST.get('valor')
        gasto.Data = request.POST.get('data')
        cat = Categoria_Financeira.objects.get(id=request.POST.get('categoria'))
        gasto.Categoria_Financeira = cat
        gasto.Usuario = request.user.username
        gasto.save()
        return redirect('listaEmpreendimento')

    template_name = 'appteste/Gastos/atualizaGastos.html'
    emp = Empreendimento.objects.get(id=gasto.Empreendimento_id.id)
    cat = Categoria_Financeira.objects.all()
    context = {'gasto': gasto, 'empreendimentos': emp, 'cat': cat}
    return render(request, template_name, context)

#============================================================================

#=============================== GENÉRICAS =================================

# Retorna as cidades de um estado
def retornaCidades(request, uf):
    cidades = ufbr.list_cidades(uf)
    json_lst = json.dumps(cidades, ensure_ascii=False)
    return HttpResponse(json_lst)

# Lista de categorias de usuários
def listaCategorias(request):
    obj = Categoria_Usuario.objects.filter(Ativa=True)
    template_name = "appteste/Usuario/manutencaoUsuario.html"
    context = {"obj": obj}
    return render(request, template_name, context)

    categoria = request.POST.get('categoria')
    data1 = request.POST.get('data1')
    data2 = request.POST.get('data2')
    empreendimento = request.POST.get('empreendimento')
    gastos = Mov_Financeira.objects.filter(A_pagar = True)
    if (categoria != ""):
        gastos = gastos.filter(Categoria_Financeira = categoria)
    if (data1 != "" or data2 != ""):
        gastos = gastos.filter(Data__date__range = (data1, data2))
    if (empreendimento != ""):
        gastos = gastos.filter(Empreendimento_id = empreendimento)
    
    emp = Empreendimento.objects.filter(Ativo=True)
    categorias = Categoria_Financeira.objects.filter(Ativa=True)
    context = {'gastos': gastos, 'emp': emp, 'categorias': categorias}
    
    return render(request, 'appteste/Gastos/listaGastos.html', context)
#============================================================================