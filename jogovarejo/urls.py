from django.urls import path, re_path

from . import views

app_name = "jogovarejo"
urlpatterns = [
    path ('',                           views.index,             name='index'),     
    path ('formula/<int:numeroGrupo>/', views.detalheFormulacao, name="detalheFormulacao"), 
    path ('salvametodo/',               views.salvaMetodo,       name='salvaMetodo'),
    path ('simula/<int:numeroGrupo>/',  views.detalheSimulacao,  name="detalheSimulacao"), 
    path ('avancadia/',                 views.avancaUmDia,       name='avancaUmDia'),
    path ('retrocede1dia/',             views.retrocedeUmdia,    name='retrocedeUmdia'),
    path ('avalia/<int:numeroGrupo>/',  views.detalheAvaliacao,  name="detalheAvaliacao"), 
    path ('decisoes/',                  views.decisoesDosGrupos, name='decisoesDosGrupos'), 
    path ('avanca/',                    views.avancaFase,        name='avancaFase'), 
    path ('retrocede/',                 views.retrocedeFase,     name='retrocedeFase'), 
    path ('sobre/',                     views.sobre,             name='sobre'),
    re_path(r'^.*\.*', views.pages, name='pages'),  # Essa linha precisa ser a última porque é ela que trata as URLs inexistentes (todas não tratadas até ela)   
] 
