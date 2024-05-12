import random

def sortear():
    # Inicializa
    random.seed()

    # Obtém numero aleatório entre 0 e 1 e depois determina Prazo sorteado
    NAleatorio = random.random()
    if NAleatorio <= 0.6:
        prazo = 1
    else:
        prazo = 2

    # Obtém numero aleatório entre 0 e 1 e depois determina Faixa de demanda sorteada
    NAleatorio = random.random()
    if NAleatorio <= 0.05:
        demanda = 21
    elif NAleatorio <= 0.2:
        demanda = 26
    elif NAleatorio <= 0.5:
        demanda = 31
    elif NAleatorio <= 0.7:
        demanda = 36
    elif NAleatorio <= 0.9:
        demanda = 41
    else:
        demanda = 46

    # Obtém numero aleatório entre 0 e 1 e depois determina Demanda dentro da faixa sorteada
    NAleatorio = random.random()
    if NAleatorio <= 0.2:
        demanda = demanda + 0
    elif NAleatorio <= 0.4:
        demanda = demanda + 1
    elif NAleatorio <= 0.6:
        demanda = demanda + 2
    elif NAleatorio <= 0.8:
        demanda = demanda + 3
    else:
        demanda = demanda + 4
    
    return prazo, demanda
