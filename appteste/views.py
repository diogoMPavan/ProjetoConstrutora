from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from datetime import datetime
from pyUFbr.baseuf import ufbr
from .models import Empreendimento, Mov_Financeira, Categoria_Financeira
from appteste.forms import RegisterUserForm
from django.contrib.auth.forms import UserCreationForm

#============================== Abre telas ==================================

# Home
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html') 
    else:
        return redirect("login")

# Tela de login
def login_view(request):
    return render(request, 'registration/login.html')

# Lista de Usuários
def listaUsuario(request):
    usr = get_user_model()
    obj = usr.objects.filter(is_active=True)
    template_name = "appteste/Usuario/listaUsuario.html"
    context = {"usr": obj}

    if request.user.is_authenticated:
        return render(request, template_name, context)
    else:
        return redirect('login')

# Lista de Empreendimentos com busca
def listaEmpreendimento(request):
    # Pega os parâmetros de pesquisa
    nome = request.GET.get('nome', '')
    descricao = request.GET.get('descricao', '')
    uf = request.GET.get('uf', '')
    cidade = request.GET.get('cidade', '')

    # Filtragem de empreendimentos com base nos parâmetros
    empreendimentos = Empreendimento.objects.filter(Ativo=True)

    # Aplicando os filtros, se os campos de pesquisa estiverem preenchidos
    if nome:
        empreendimentos = empreendimentos.filter(Nome__icontains=nome)
    if descricao:
        empreendimentos = empreendimentos.filter(Descricao__icontains=descricao)
    if uf:
        empreendimentos = empreendimentos.filter(UF__icontains=uf)
    if cidade:
        empreendimentos = empreendimentos.filter(Cidade__icontains=cidade)

    # Paginação
    paginator = Paginator(empreendimentos, 5)  # 5 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Movimentos financeiros pendentes
    mov_fin = Mov_Financeira.objects.filter(A_pagar=True)

    # Contexto para passar para o template
    context = {
        "emp": page_obj,
        "mov_fin": mov_fin,
        "nome": nome,
        "descricao": descricao,
        "uf": uf,
        "cidade": cidade,
    }

    if request.user.is_authenticated:
        return render(request, 'appteste/Empreendimento/listaEmpreendimento.html', context)
    else:
        return redirect('login')


# Cadastro de Empreendimento
def cadEmpreendimento(request):
    obj = Empreendimento.objects.filter(Ativo=True)
    context = {"obj": obj, "uf": ufbr.list_uf}
    
    if request.user.is_authenticated:
        return render(request, 'appteste/Empreendimento/manutencaoEmpreendimento.html', context) 
    else:
        return redirect('login')

# Cadastro de Gastos
def cadGastos(request, f_id):
    emp = Empreendimento.objects.get(id=f_id)
    cat = Categoria_Financeira.objects.filter(Ativa=True)
    context = {'empreendimentos': emp, 'categoria': cat}
    
    if request.user.is_authenticated:
        return render(request, 'appteste/Gastos/cadGastos.html', context)
    else:
        return redirect('login')

#============================================================================

#========================== USUÁRIO ================================

# Cadastro de novo usuário
def cadUsuario(request):
    if request.method == 'POST':
        group = request.user.groups
        print(group)  # Para depuração
        if group == 'ADMIN':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuário criado com sucesso!")
                return redirect("listaUsuario")
        else:
            messages.error(request, "Seu usuário não tem permissão para criar um novo usuário")
            return redirect("listaUsuario")
    else:
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)

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
def deleteUsuario(request, f_id):
    usuario = Usuario.objects.get(id=f_id)
    if request.method == "POST":
        usuario.Ativo = False
        usuario.save()
        return redirect('listaUsuario')
    
    template_name = "appteste/Usuario/confirmacaoUsuario.html"
    context = {"usuario": usuario}
    return render(request, template_name, context)
    
# Atualiza os dados do usuário
def updateUsuario(request, f_id):
    usuario = User.objects.get(id=f_id)
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("listaUsuario")
    
    template_name = "appteste/Usuario/updateUser.html"
    form = RegisterUserForm()
    return render(request, template_name, {"usuario": usuario, "form": form})

#============================================================================

#===================================== EMPREENDIMENTO =======================================

# Salva um novo empreendimento
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
def listaGastos(request):
    gastos = Mov_Financeira.objects.filter(A_pagar=True).order_by('Empreendimento_id')
    emp = Empreendimento.objects.all()
    context = {'gastos': gastos, 'emp': emp}
    
    if request.user.is_authenticated:
        return render(request, 'appteste/Gastos/listaGastos.html', context)
    else:
        return redirect('login')

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

#============================================================================