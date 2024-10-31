from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("cadUsuario/", views.cadUsuario, name="cadUsuario"),
    path("cadUsuario2/", views.cadUsuario2, name="cadUsuario2"),
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
    path('salvaGastos/', views.salvaGastos, name='salvaGastos'),
    path('listaGastos/', views.listaGastos, name='listaGastos'),
    path('deleteGasto/<int:f_id>', views.deleteGasto, name='deleteGasto'),
    path('updateGasto/<int:f_id>', views.updateGasto, name='updateGasto'),
    #=========================================================================
    path('cadEmpreendimento/', views.cadEmpreendimento, name="cadEmpreendimento"),
    path('listaEmpreendimento/', views.listaEmpreendimento, name="listaEmpreendimento"),
    path('retornaCidades/<str:uf>/', views.retornaCidades, name="retoraCidades"),
]