from django.db.models import Sum
from jogovarejo.models import Controle, Grupo, Sorteado, Movimento, Compra
from decimal import Decimal, ROUND_HALF_UP


def InicializaNovoDia (grGerente, diaCorrente, SaldoFinalDiaCorrente):
    # Inicializa movimento correspondente ao proximo dia:
    novoDia  = diaCorrente + 1
    novoMovi = Movimento (Grupo=grGerente,  Dia=novoDia)
    novoMovi.Recebido     = Compra.objects.filter (Grupo=grGerente, DiaEntrega=novoDia).aggregate(Sum('QuantCompra', default=0))['QuantCompra__sum']
    novoMovi.AReceber     = Compra.objects.filter (Grupo=grGerente, DiaEntrega__gt=novoDia).aggregate(Sum('QuantCompra', default=0))['QuantCompra__sum']
    novoMovi.SaldoInicial = SaldoFinalDiaCorrente + novoMovi.Recebido
    novoMovi.save() 


def ProcessaUmDia (grGerente, decisaoDeCompra):
    diaFimDeJogo = Controle.objects.filter (Nome='Ativo').first().Duracao
    diaCorrente  = grGerente.DiaCorrente
    movi         = Movimento.objects.get (Grupo=grGerente, Dia=diaCorrente)
    sorteado     = Sorteado.objects.get (Dia=diaCorrente)

    # Atribui demais campos do movimento do dia corrente (que será encerrado):
    movi.Comprado = decisaoDeCompra
    movi.Prazo    = sorteado.PrazoSorteado
    movi.Demanda  = sorteado.DemandaSorteada
    if movi.Demanda < movi.SaldoInicial:
        movi.Vendido = movi.Demanda
    else:
        movi.Vendido = movi.SaldoInicial
    movi.SaldoFinal    = movi.SaldoInicial - movi.Vendido
    movi.SaldoMedioDia = Decimal (movi.SaldoInicial + movi.SaldoFinal).quantize(Decimal('0.1'), ROUND_HALF_UP) / 2
    movi.save() 

    # Registra nova compra na tabela de compras:
    if movi.Comprado > 0:
        compra = Compra (Grupo=grGerente, DiaCompra=diaCorrente, DiaEntrega=diaCorrente+movi.Prazo, QuantCompra=movi.Comprado)
        compra.save() 

    # inicializa movimento correspondente ao proximo dia (caso não seja fim de jogo):
    if diaCorrente < diaFimDeJogo:
        InicializaNovoDia (grGerente, diaCorrente, movi.SaldoFinal) 
        return "Dia processado com sucesso."
    else:
        return "Dia processado com sucesso. Simulação concluida."


def RetrocedeUmDia (grGerente):
    diaFimDeJogo = Controle.objects.filter (Nome='Ativo').first().Duracao
    diaCorrente  = grGerente.DiaCorrente
    if diaCorrente > 1:
        # Exclui "movimento" do último dia (que se encontra simplesmente inicializado), 
        # exceto se é fim do jogo (porque nesse caso não há registro a excluir):
        movi = Movimento.objects.get (Grupo=grGerente, Dia=diaCorrente)
        if (diaCorrente < diaFimDeJogo) or ((diaCorrente == diaFimDeJogo) and (movi.Demanda is None)):
            movi.delete()  
        # Apaga valores que expressam "processamento" do ultimo dia processado:
        novoDiaCorrente  = grGerente.DiaCorrente
        movi = Movimento.objects.get (Grupo=grGerente, Dia=novoDiaCorrente)  
        movi.Comprado      = None
        movi.Prazo         = None
        movi.Demanda       = None
        movi.Vendido       = None
        movi.SaldoFinal    = None
        movi.SaldoMedioDia = None
        movi.save() 
        # Exclui última "compra", caso exista, do mesmo dia do movimento "desprocessado" acima:
        compra = Compra.objects.filter (Grupo=grGerente, DiaCompra=novoDiaCorrente).first()
        if compra is not None:
            compra.delete()
        return "Retrocedido um dia com sucesso."
    else:
        return "Não há nenhum dia processado."
