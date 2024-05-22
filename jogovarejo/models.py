from django.db import models
from django.db.models import Max, Sum
from decimal import Decimal, ROUND_HALF_UP


class Controle (models.Model):
    Nome                 = models.CharField    (max_length=30,  unique=True) # Haverá 1 só registro c/ nome "Ativo"
    Fase                 = models.IntegerField ("fase corrente em execução", default=  1)
    Duracao              = models.IntegerField ("número de dias do jogo",    default= 40)
    PrecoCompra          = models.DecimalField ("preço de compra",           max_digits=5, decimal_places=2, 
                                                                             default=0.5)
    PrecoVenda           = models.DecimalField ("preço de venda",            max_digits=5, decimal_places=2, 
                                                                             default=  2)
    CustoFixoDiario      = models.DecimalField ("custo fixo diario",         max_digits=5, decimal_places=2, 
                                                                             default=  5)
    CustoUnitarioFrete   = models.DecimalField ("custo unitario frete",      max_digits=5, decimal_places=2, 
                                                                             default= 10)
    CustoUnitarioEstocar = models.DecimalField ("custo unitario de estocar", max_digits=5, decimal_places=2, 
                                                                             default=0.1)
    GanhoUnitario        = models.DecimalField ("ganho unitario",            max_digits=5, decimal_places=2, 
                                                                             default=1.5)
    DemandaMediaDiária   = models.DecimalField ("demanda media diária",      max_digits=5, decimal_places=2, 
                                                                             default= 36)
    DiasNoAno            = models.IntegerField ("número de dias no ano",     default=360)

    def __str__(self):
        return self.Nome


class Sorteado (models.Model):
    Dia             = models.IntegerField ()
    PrazoSorteado   = models.IntegerField ("prazo sorteado")
    DemandaSorteada = models.IntegerField ("demanda Sorteada")


class Grupo (models.Model):
    Numero        = models.IntegerField ("número do grupo", default=0)
    Nome          = models.CharField  (max_length= 20, unique=True)
    Quando        = models.TextField  (max_length=800, blank=True)
    Quanto        = models.TextField  (max_length=800, blank=True)
    Ativo         = models.BooleanField ("está participando do jogo") 
    Fase1Ok       = models.BooleanField ("decidiu método de gestão", default=False) 
    GrupoOperador = models.ForeignKey ('self',  
                                       models.SET_NULL,      # p/campo assumir "null" se objeto associado for excluido
                                       blank=True, null=True, 
                                       related_name='operadorGrupo')
    @property
    def DiaCorrente (self):
        return Movimento.objects.filter (Grupo=self).aggregate (Max('Dia')) ['Dia__max']

    @property
    def DiaCorrenteDoGrupoComoOperador (self):
        grGerente  = Grupo.objects.filter (GrupoOperador=self).first()
        return grGerente.DiaCorrente

    @property
    def Fase2DoGrupoComoOperadorOk (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        if self.DiaCorrenteDoGrupoComoOperador == ct.Duracao:
            grGerente  = Grupo.objects.filter (GrupoOperador=self).first()
            ultimoMovi = Movimento.objects.filter (Grupo=grGerente, Dia=ct.Duracao).first()
            if ultimoMovi.Demanda is not None:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return self.Nome


class Movimento (models.Model):
    Grupo         = models.ForeignKey   (Grupo, on_delete=models.CASCADE, 
                                         related_name='grupoMovimento')
    Dia           = models.IntegerField ()
    Recebido      = models.IntegerField ("quantidade recebida")
    AReceber      = models.IntegerField ("quantidade a receber")
    SaldoInicial  = models.IntegerField ("saldo inicial")
    Comprado      = models.IntegerField ("quantidade comprada",  null=True)
    Prazo         = models.IntegerField ("prazo de entrega",     null=True)
    Demanda       = models.IntegerField ("quantidade demandada", null=True)
    Vendido       = models.IntegerField ("quantidade vendida",   null=True)
    SaldoFinal    = models.IntegerField ("saldo final",          null=True)
    SaldoMedioDia = models.DecimalField ("saldo médio",          null=True, max_digits=5, decimal_places=1)
    
    @property
    def SaldoFinalAnterior (self):
        if self.Dia > 1: sdAnterior = Movimento.objects.get (Grupo=self.Grupo, Dia=self.Dia-1).SaldoFinal
        else:            sdAnterior = 80
        return sdAnterior


class Compra (models.Model):
    Grupo       = models.ForeignKey   (Grupo, on_delete=models.CASCADE, 
                                       related_name='grupoCompra')
    DiaCompra   = models.IntegerField ("dia da compra")
    DiaEntrega  = models.IntegerField ("dia da entrega")
    QuantCompra = models.IntegerField ("quantidade comprada")
    # HouveFalta  = models.BooleanField ("ocorreu falta", null=True) # Enquanto for "Null" compra não chegou

    @property
    def HouveFalta (self):
        moviInicioTR = Movimento.objects.get (Grupo=self.Grupo, Dia=self.DiaCompra)
        providenciadoInicioTR = moviInicioTR.SaldoInicial + moviInicioTR.AReceber
        DemandaDuranteTR = Movimento.objects.filter (Grupo=self.Grupo, Dia__gte=self.DiaCompra, Dia__lt=self.DiaEntrega).aggregate (Sum('Demanda', default=0)) ['Demanda__sum']
        if providenciadoInicioTR < DemandaDuranteTR:
            return True
        else:
            return False


class IndicadoresDoGrupo (Grupo):
    # Sub-classe do grupo onde todos os campos são calculados
    class Meta:
        proxy = True    # Indicando que este é um "proxy model", ou
        verbose_name        = "indicadores de resultado do grupo"
        verbose_name_plural = "indicadores de resultado dos grupos"

    # Dados da Simulação:
    @property
    def Duracao (self):
        hoje       = self.DiaCorrente
        ultimoMovi = Movimento.objects.get (Grupo=self, Dia=hoje)
        if ultimoMovi.Demanda is None:
            return hoje - 1
        else:
            return hoje
    
    @property
    def DemandaTotal (self):
        return Movimento.objects.filter (Grupo=self).aggregate (Sum('Demanda', default=0)) ['Demanda__sum']
    
    @property
    def DemandaMedia (self):
        if self.Duracao == 0: 
            return Decimal (0)
        else: 
            return (Decimal(self.DemandaTotal) / Decimal(self.Duracao)).quantize (Decimal('0.1'),ROUND_HALF_UP) # Obs.1: Inteiros devem 
                            # ser transformados em decimal antes de serem divididos para que o resultado da divisão não seja do tipo "float".
                            # Obs.2: "0.1" é usado p/estabelecer o número de casas decimais (poderia ser "9.9" ou quaisquer algarismos).
                            # Obs.3: "ROUND_HALF_UP" é p/arredondar p/o mais próximo e p/cima quando no meio exato.

    @property
    def TRMedio (self):
        if self.Duracao == 0: 
            return Decimal (0)
        else:
            soma = Movimento.objects.filter (Grupo=self).aggregate (Sum('Prazo', default=0)) ['Prazo__sum']
            return (Decimal(soma) / Decimal(self.Duracao)).quantize (Decimal('0.01'),ROUND_HALF_UP)


    # Atendimento aos Clientes:
    @property
    def ClientesAtendidos (self):
        return Movimento.objects.filter (Grupo=self).aggregate (Sum('Vendido', default=0)) ['Vendido__sum']
    
    @property
    def Ganho (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.ClientesAtendidos * ct.GanhoUnitario).quantize (Decimal('1'), ROUND_HALF_UP)
    
    @property
    def ClientesPerdidos (self):
        return self.DemandaTotal - self.ClientesAtendidos
    
    @property
    def GanhoPerdido (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.ClientesPerdidos * ct.GanhoUnitario).quantize (Decimal('1'), ROUND_HALF_UP)
    
    @property
    def NivelServicoCliente (self):
        if self.DemandaTotal == 0: 
            return Decimal (0)
        else:
            return (Decimal(self.ClientesAtendidos) * 100  / Decimal(self.DemandaTotal)).quantize (Decimal('0.1'), ROUND_HALF_UP)


    # Estoque Médio:
    def EstqMedNãoArredond (self):
        if self.Duracao == 0: 
            return Decimal (0)
        else:
            soma = Movimento.objects.filter (Grupo=self).aggregate (Sum('SaldoMedioDia', default=0)) ['SaldoMedioDia__sum']
            return soma / self.Duracao

    @property
    def EstoqueMedio (self):
        return (self.EstqMedNãoArredond()).quantize (Decimal('1'), ROUND_HALF_UP)
    
    @property
    def CoberturaEstoqueMedio (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.EstqMedNãoArredond() / ct.DemandaMediaDiária).quantize (Decimal('0.01'), ROUND_HALF_UP)
    
    @property
    def CapitalEstoqueMedio (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.EstqMedNãoArredond() * ct.PrecoCompra).quantize (Decimal('0.1'), ROUND_HALF_UP)
    
    @property
    def CustoEstocar (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.EstqMedNãoArredond() * self.Duracao * ct.CustoUnitarioEstocar).quantize (Decimal('1'), ROUND_HALF_UP)
    
    @property
    def Giro (self):
        if (self.EstoqueMedio == 0) or (self.Duracao == 0): 
            return Decimal (0)
        else:
            ct = Controle.objects.filter (Nome='Ativo').first()
            return (Decimal(self.DemandaTotal * ct.DiasNoAno) / Decimal(self.Duracao)  / self.EstqMedNãoArredond()).quantize (Decimal('0.1'), ROUND_HALF_UP)


    # Estoque Máximo:
    @property
    def EstoqueMaximo (self):
        return Movimento.objects.filter (Grupo=self).aggregate (Max('SaldoInicial', default=0)) ['SaldoInicial__max']

    @property
    def CoberturaEstoqueMaximo (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (Decimal(self.EstoqueMaximo) / Decimal(ct.DemandaMediaDiária)).quantize(Decimal('0.1'), ROUND_HALF_UP)

    @property
    def CapitalEstoqueMaximo (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.EstoqueMaximo * ct.PrecoCompra).quantize (Decimal('0.1'), ROUND_HALF_UP)


    # Suprimentos:
    @property
    def NumeroEncomendas (self):
        return Compra.objects.filter (Grupo=self, DiaEntrega__lte=self.Duracao).count()

    @property
    def CustoFrete (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.NumeroEncomendas * ct.CustoUnitarioFrete).quantize (Decimal('1'), ROUND_HALF_UP)

    @property
    def QuebrasDeEstoque (self):
        compras = Compra.objects.filter (Grupo=self, DiaEntrega__lte=self.Duracao)
        comprasComFalta = [compra for compra in compras if compra.HouveFalta]
        return len (comprasComFalta)

    @property
    def NivelServiçoSuprimentos (self):
        if self.NumeroEncomendas == 0: 
            return Decimal (0)
        else: 
            return (Decimal((self.NumeroEncomendas - self.QuebrasDeEstoque) * 100) / Decimal(self.NumeroEncomendas)).quantize(Decimal('0.1'), ROUND_HALF_UP)

    # Apuração do Resultado:
    @property
    def GanhoPotencial (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.DemandaTotal * ct.GanhoUnitario).quantize (Decimal('1'), ROUND_HALF_UP)

    @property
    def CustoGerenciado (self):
        return (self.GanhoPerdido + self.CustoEstocar + self.CustoFrete).quantize (Decimal('1'), ROUND_HALF_UP)

    @property
    def CustoFixo (self):
        ct = Controle.objects.filter (Nome='Ativo').first()
        return (self.Duracao * ct.CustoFixoDiario).quantize (Decimal('1'), ROUND_HALF_UP)

    @property
    def Lucro (self):
        return (self.GanhoPotencial - self.CustoGerenciado - self.CustoFixo).quantize (Decimal('1'), ROUND_HALF_UP)

    @property
    def Lucratividade (self):
        if self.CapitalEstoqueMedio == 0: 
            return Decimal (0)
        else:
            return (self.Lucro / self.CapitalEstoqueMedio).quantize (Decimal('0.1'), ROUND_HALF_UP)
