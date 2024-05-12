from django.urls import path, re_path

from . import views

app_name = "jogovarejo"
urlpatterns = [
    path ('',                         views.index,             name='index'),     # ESSA LINHA NÃO FUNCIONA SE COLOCADA APÓS O "RE_PATH"
    path ('fase1/<int:numeroGrupo>/', views.detalheGrupoFase1, name="detalheGrupoFase1"), 
    path ('salvametodo/',             views.salvaMetodo,       name='salvaMetodo'),
    path ('fase2/<int:numeroGrupo>/', views.detalheGrupoFase2, name="detalheGrupoFase2"), 
    path ('avancadia/',               views.avancaUmDia,       name='avancaUmDia'),
    path ('retrocede1dia/',           views.retrocedeUmdia,    name='retrocedeUmdia'),
    path ('fase3/<int:numeroGrupo>/', views.detalheGrupoFase3, name="detalheGrupoFase3"), 
    path ('avanca/',                  views.avancaFase,        name='avancaFase'), 
    path ('retrocede/',               views.retrocedeFase,     name='retrocedeFase'), 
    path ('sobre/',                   views.sobre,             name='sobre'),
    re_path(r'^.*\.*', views.pages, name='pages'),
] 
