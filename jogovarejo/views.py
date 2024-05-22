from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django import template
from django.template import loader
from rest_framework import viewsets, permissions

from .models import Controle, Grupo, Movimento, IndicadoresDoGrupo
from .dinamica import ProcessaUmDia, RetrocedeUmDia
from .serializers import IndicadoresSerializer, GruposSerializer


def numeroGrupoDoUsuario (loginUsuario):
    if loginUsuario   == 'grupo1':  numGrupo = 1
    elif loginUsuario == 'grupo2':  numGrupo = 2
    elif loginUsuario == 'grupo3':  numGrupo = 3
    elif loginUsuario == 'grupo4':  numGrupo = 4
    elif loginUsuario == 'grupo5':  numGrupo = 5
    elif loginUsuario == 'grupo6':  numGrupo = 6
    elif loginUsuario == 'grupo7':  numGrupo = 7
    elif loginUsuario == 'grupo8':  numGrupo = 8
    elif loginUsuario == 'grupo9':  numGrupo = 9
    elif loginUsuario == 'grupo10': numGrupo = 10
    elif loginUsuario == 'grupo11': numGrupo = 11
    elif loginUsuario == 'grupo12': numGrupo = 12
    return numGrupo


@login_required(login_url="/login/")
def index (request):
    loginUsuario = request.user.username
    if loginUsuario == 'professor':
        controle = Controle.objects.filter (Nome='Ativo').first()
        grupos = Grupo.objects.filter (Ativo=True).order_by ('Numero')
        contexto = {'tela'   : 'professor', 
                    'fase'   : controle.Fase,
                    'grupos' : grupos}
        return render (request, 'jogovarejo/index.html', contexto)
    else:
        numGrupo = numeroGrupoDoUsuario (loginUsuario)
        fase = Controle.objects.filter (Nome='Ativo').first().Fase
        if fase == 1:
            return HttpResponseRedirect (reverse ('jogovarejo:detalheFormulacao', args=(str(numGrupo))))
        elif fase == 2:
            return HttpResponseRedirect (reverse ('jogovarejo:detalheSimulacao', args=(str(numGrupo))))
        elif fase == 3:
            return HttpResponseRedirect (reverse ('jogovarejo:detalheAvaliacao', args=(str(numGrupo))))


@login_required(login_url="/login/")
def salvaMetodo (request):
    if request.method == 'POST':
        numGrupo = request.POST.get('numGrupo')
        quando   = request.POST.get('quando')
        quanto   = request.POST.get('quanto')
        try:
            grupo = Grupo.objects.get(Numero=numGrupo)
            grupo.Quando  = quando
            grupo.Quanto  = quanto
            grupo.Fase1Ok = True
            grupo.save()
            messages.success (request, 'Gravação bem sucedida! Aguarde a Fase 2 ou altere seu método, se desejar.')
        except ObjectDoesNotExist:
            messages.error (request, 'Aconteceu algo de errado. Tente de novo por favor')
    return HttpResponseRedirect (reverse ('jogovarejo:detalheFormulacao', args=(numGrupo)))


@login_required(login_url="/login/")
def detalheFormulacao (request, numeroGrupo):
    controle   = Controle.objects.filter (Nome='Ativo').first()
    grupo      = Grupo.objects.get(Numero=numeroGrupo)
    contexto = {'tela'       : 'alunoFormulacao', 
                'fase'       : controle.Fase,
                'grupo'      : grupo}
    return render (request, 'jogovarejo/detalheformula.html', contexto)


@login_required(login_url="/login/")
def avancaUmDia (request):
    if request.method == 'POST':
        numGrupo        = request.POST.get('numGrupo')
        diaNaEstacaoStr = request.POST.get('diaCorrenteNaEstacao')
        quantidadeStr   = request.POST.get('novaCompra')
        try:
            grOperador = Grupo.objects.get (Numero=numGrupo)
            grGerente  = Grupo.objects.filter (GrupoOperador=grOperador).first()
            diaNaEstacao = int (diaNaEstacaoStr)
            if diaNaEstacao == grGerente.DiaCorrente:
                try:
                    quantidade = int (quantidadeStr)
                    if quantidade >= 0:
                        mensagem = ProcessaUmDia (grGerente, quantidade)
                        messages.success (request, mensagem)
                    else:
                        messages.error (request, 'Edição inválida. Tente de novo')
                except ValueError:
                    messages.error (request, 'Edição inválida. Tente de novo')
            else:
                messages.error (request, 'Data inválida.')
        except ValueError or ObjectDoesNotExist:
            messages.error (request, 'Aconteceu algo de errado. Tente de novo por favor')
    return HttpResponseRedirect (reverse ('jogovarejo:detalheSimulacao', args=(numGrupo)))


@login_required(login_url="/login/")
def retrocedeUmdia (request):
    if request.method == 'POST':
        numGrupo = request.POST.get('numGrupo')
        try:
            grOperador = Grupo.objects.get (Numero=numGrupo)
            grGerente  = Grupo.objects.filter (GrupoOperador=grOperador).first()
            mensagem = RetrocedeUmDia (grGerente)
            messages.success (request, mensagem)
        except ObjectDoesNotExist:
            messages.error (request, 'Aconteceu algo de errado. Tente de novo por favor')
    return HttpResponseRedirect (reverse ('jogovarejo:detalheSimulacao', args=(numGrupo)))


@login_required(login_url="/login/")
def detalheSimulacao (request, numeroGrupo):
    controle   = Controle.objects.filter (Nome='Ativo').first()
    grupo      = Grupo.objects.get(Numero=numeroGrupo)  # "grupo" é o grupo operador
    grGerente  = Grupo.objects.filter (GrupoOperador=grupo).first()
    moviDeHoje = Movimento.objects.filter(Grupo=grGerente, Dia=grGerente.DiaCorrente).first()
    historico  = Movimento.objects.filter (Grupo=grGerente).order_by ('Dia')
    contexto = {'tela'       : 'alunoSimulacao', 
                'fase'       : controle.Fase,
                'grupo'      : grupo,    # "grupo" é o grupo operador
                'hoje'       : grupo.DiaCorrenteDoGrupoComoOperador, 
                'grGerente'  : grGerente,
                'moviDeHoje' : moviDeHoje,
                'historico'  : historico}
    return render (request, 'jogovarejo/detalhesimula.html', contexto)


@login_required(login_url="/login/")
def detalheAvaliacao (request, numeroGrupo):
    controle   = Controle.objects.filter (Nome='Ativo').first()
    grupo      = IndicadoresDoGrupo.objects.get(Numero=numeroGrupo)
    historico  = Movimento.objects.filter (Grupo=grupo).order_by ('Dia')
    contexto = {'tela'       : 'alunoAvaliacao', 
                'fase'       : controle.Fase,
                'grupo'      : grupo,
                'hoje'       : grupo.DiaCorrente, 
                'historico'  : historico}
    return render (request, 'jogovarejo/detalheavalia.html', contexto)


def obtemDecisoesDosGrupos ():
    controle   = Controle.objects.filter (Nome='Ativo').first()
    grupos = Grupo.objects.filter (Ativo=True).order_by ('Numero')
    # Cria primeira linha (que será mostrada como primeira coluna) para mostrar os dias:
    decisoes = []
    decisoesGrupo = ['Dia']
    for dia in range (1, controle.Duracao+1):
        decisoesGrupo.append (dia)
    decisoes.append (decisoesGrupo)
    # Inicializa restante da matriz com nome dos grupos e decisão "-1":
    for grupo in grupos:
        decisoesGrupo = [grupo.Numero]
        for dia in range (1, controle.Duracao+1):
            decisoesGrupo.append (-1)
        decisoes.append (decisoesGrupo)
    # Agora obtem e atribui decisoes:
    for grupo in grupos:
        historico  = Movimento.objects.filter (Grupo=grupo).order_by ('Dia')
        for histDia in historico:
            if histDia.Comprado != None:
                decisoes [grupo.Numero] [histDia.Dia] = histDia.Comprado
    # Por fim transpõe a matriz, pois será construida linha a linha (grupos nas colunas, dias nas linhas)
        decisoes_transpostas = list (map (list, zip(*decisoes)))
        # Para entender o comando acima:
        # - o operador "*" desempacota a "lista de lista" em "listas"
        # - a função "zip" transpõe os elementos das listas recebidas retornando-as como tuplas
        # - a função "list" mais interna transforma uma tupla em uma lista
        # - a função "map" aplica a função "list" a cada uma das tuplas transformando-as, portanto, em listas
        # - a função "list" mais externa, por fim, transforma o conjunto de listas em uma lista de listas
    return decisoes_transpostas


@login_required(login_url="/login/")
def decisoesDosGrupos (request):
    controle = Controle.objects.filter (Nome='Ativo').first()
    contexto = {'tela'     : 'decisoes',
                'fase'     : controle.Fase,
                'decisoes' : obtemDecisoesDosGrupos}
    return render (request, 'jogovarejo/decisoes.html', contexto)


@login_required(login_url="/login/")
def avancaFase (request):
    if request.method == 'POST':
        controle = Controle.objects.filter (Nome='Ativo').first()
        if controle.Fase < 3:
            controle.Fase += 1
            controle.save()
            messages.success (request, 'Fase avançada com sucesso')
        else:
            messages.error (request, 'Não foi possivel avançar de fase')
    return HttpResponseRedirect (reverse ('jogovarejo:index'))


@login_required(login_url="/login/")
def retrocedeFase (request):
    if request.method == 'POST':
        controle = Controle.objects.filter (Nome='Ativo').first()
        if controle.Fase > 1:
            controle.Fase -= 1
            controle.save()
            messages.success (request, 'Fase retrocedida com sucesso')
        else:
            messages.error (request, 'Não foi possivel retroceder fase')
    return HttpResponseRedirect (reverse ('jogovarejo:index'))


@login_required(login_url="/login/")
def sobre (request):
    contexto = {'tela' : 'sobre'}
    return render (request, 'jogovarejo/sobre.html', contexto)



# Endpoint de API que permite acesso de leitura aos indicadores dos grupos:
class GruposViewSet (viewsets.ReadOnlyModelViewSet):
    queryset = Grupo.objects.filter (Ativo=True).order_by ("Numero")
    serializer_class = GruposSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]


# Endpoint de API que permite acesso de leitura aos indicadores dos grupos:
class IndicadoresViewSet (viewsets.ReadOnlyModelViewSet):
    queryset = IndicadoresDoGrupo.objects.filter (Ativo=True).order_by ("Numero")
    serializer_class = IndicadoresSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    # except:
        # html_template = loader.get_template('home/page-500.html')
        # return HttpResponse(html_template.render(context, request))
