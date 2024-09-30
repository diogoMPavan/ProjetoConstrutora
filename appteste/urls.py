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
]