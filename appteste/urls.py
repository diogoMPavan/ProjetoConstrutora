from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),

    path("login/", views.login, name="login"),
    path("cadUsuario/", views.cadUsuario, name="cadUsuario"),
    path("listaUsuario/", views.listaUsuario, name="listaUsuario"),
    path("listaEmpreendimento/", views.listaEmpreendimento, name="listaEmpreendimento"),
    path("categorias/", views.listaCategorias, name="lista_categorias"),
    path("mostraCategorias/", views.mostraCategoria, name="mostraCategorias"),
    path('cadGastos/<int:f_id>', views.cadGastos, name="cadGastos"),
    #============================= USUARIO ===================================
    path("appteste/salvaUsuario/", views.salvaUsuario, name="salvaUsuario"),
    path("mostrarUsuarios/", views.mostrarUsuarios, name="mostrar"),
    path('update/<int:f_id>', views.updateUsuario, name="updateUsuario"),
    path('del/<int:f_id>', views.deleteUsuario, name="deleteUsuario"),
    #=========================================================================
    #============================= EMPREENDIMENTO ============================
    path('salvaEmpreendimento/', views.salvaEmpreendimento, name="salvaEmpreendimento"),
    path('delEmp/<int:f_id>', views.deleteEmpreendimento, name="deleteEmp"),
    path('updateEmp/<int:f_id>', views.updateEmpreendimento, name="updateEmp"),
    #=========================================================================
    #================================= GASTOS ================================

    #=========================================================================
    path('fazLogin/', views.fazLogin, name="fazLogin"),
    path('cadEmpreendimento/', views.cadEmpreendimento, name="cadEmpreendimento"),
    path('listaEmpreendimento/', views.listaEmpreendimento, name="listaEmpreendimento"),
    path('retornaCidades/<str:uf>/', views.retornaCidades, name="retoraCidades"),
]