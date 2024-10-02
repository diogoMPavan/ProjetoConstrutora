"""
URL configuration for siteconstrutora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

#aqui é onde são colocadas as rotas que irão nortear o site
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("appteste.urls")),
    path('tinymce/', include('tinymce.urls')),
    path("login/", include("appteste.urls")),
    path("cadUsuario/", include('appteste.urls')),
    path("listaUsuario/", include('appteste.urls')),
    path("listaEmpreendimento/", include('appteste.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)