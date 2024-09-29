from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        usuario = request.POST.get('usuario')
        senha =request.POST.get('senha')
    
    novo_usuario = Usuario(nome=nome, login=usuario, categoria=categoria, senha=senha)
    novo_usuario.save()

    return JsonResponse({'mensagem': 'Usuario criado com sucesso!'}, status=201)