from rest_framework import serializers
from django.contrib.auth.models import User

from .models import IndicadoresDoGrupo


class GruposSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IndicadoresDoGrupo
        fields = ["Numero", "Nome"]


class IndicadoresSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IndicadoresDoGrupo
        fields = ["Numero", "Nome", 
                  # Dados da simulação:
                  "Duracao", "DemandaTotal", "DemandaMedia", "TRMedio", 
                  # Atendimento aos Clientes:
                  "ClientesAtendidos", "Ganho", "ClientesPerdidos", "GanhoPerdido", "NivelServicoCliente", 
                  # Estoque Médio:
                  "EstqMedNãoArredond", "EstoqueMedio", "CoberturaEstoqueMedio", "CapitalEstoqueMedio", "Giro", 
                  # Suprimentos:
                  "EstoqueMaximo", "CoberturaEstoqueMaximo", "CapitalEstoqueMaximo", 
                  # Suprimentos:
                  "NumeroEncomendas", "CustoFrete", "QuebrasDeEstoque", "NivelServiçoSuprimentos", 
                  # Resultado:
                  "GanhoPotencial", "CustoGerenciado", "CustoFixo", "Lucro", "Lucratividade"]