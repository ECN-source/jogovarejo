"""
URL configuration for jogovarejoweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers

from jogovarejo import views

# Modo mais simples sugerido para acesso a API:
router = routers.DefaultRouter()
router.register (r'indicadores', views.IndicadoresViewSet)
router.register (r'grupos', views.GruposViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')), # Auth routes - login / register
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # caminho p/login na API
    path('', include('jogovarejo.urls')), # Essa linha precisa ser a última porque ela contém a "re_path (...., views.pages, ....)" (que trata as URLs inexistentes)       
]
