from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("login/", views.login, name="login"),
    path("cadUsuario/", views.cadUsuario, name="cadUsuario"),
    path("listaUsuario/", views.listaUsuario, name="listaUsuario"),
    path("listaEmpreendimento/", views.listaEmpreendimento, name="listaEmpreendimento"),
    path("categorias/", views.listaCategorias, name="lista_categorias"),
    path("appteste/salvaUsuario/", views.salvaUsuario, name="salvaUsuario"),
    path("mostrarUsuarios/", views.mostrarUsuarios, name="mostrar"),
    path('del/<int:f_id>', views.deleteUsuario, name="delete"),
    path('fazLogin/', views.fazLogin, name="fazLogin"),
]