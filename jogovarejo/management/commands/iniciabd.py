from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg

from jogovarejo.models import Controle, Grupo, Sorteado, Movimento, Compra
from jogovarejo.sorteio import sortear


class Command (BaseCommand):
    help = "Reinicia banco de dados para novo jogo"

    def handle (self, *args, **options):

        # Zera conteúdo do banco de dados:
        Compra.objects.all().delete()
        Movimento.objects.all().delete()
        Sorteado.objects.all().delete()
        Grupo.objects.all().delete()
        Controle.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write (self.style.SUCCESS ('1. Zerou conteúdo do banco de dados'))
        
        # Insere usuarios:
        User.objects.create_superuser ('professor', email='professor@examplo.com', password='xadrez')
        User.objects.create_user      ('grupo1',    password='armario')
        User.objects.create_user      ('grupo2',    password='balde')
        User.objects.create_user      ('grupo3',    password='cadeira')
        User.objects.create_user      ('grupo4',    password='disco')
        User.objects.create_user      ('grupo5',    password='estante')
        User.objects.create_user      ('grupo6',    password='faca')
        User.objects.create_user      ('grupo7',    password='garfo')
        User.objects.create_user      ('grupo8',    password='helice')
        User.objects.create_user      ('grupo9',    password='indice')
        User.objects.create_user      ('grupo10',   password='janela')
        User.objects.create_user      ('grupo11',   password='livro')
        User.objects.create_user      ('grupo12',   password='mesa')
        self.stdout.write (self.style.SUCCESS ('2. Usuários do jogo recriados'))

        # Refaz tabela de Controle:
        contr = Controle (Nome='Ativo')
        contr.save() 
        self.stdout.write (self.style.SUCCESS ('3. Tabela de Controle refeita'))

        # Refaz tabela de Itens (ou grupos):
        grupo1 = Grupo  (Numero=1, Nome='Grupo 1',   Ativo=True)
        grupo1.save() 
        grupo2 = Grupo  (Numero=2, Nome='Grupo 2',   Ativo=True)
        grupo2.save() 
        grupo3 = Grupo  (Numero=3, Nome='Grupo 3',   Ativo=True)
        grupo3.save() 
        grupo4 = Grupo  (Numero=4, Nome='Grupo 4',   Ativo=True)
        grupo4.save() 
        grupo5 = Grupo  (Numero=5, Nome='Grupo 5',   Ativo=True)
        grupo5.save() 
        grupo6 = Grupo  (Numero=6, Nome='Grupo 6',   Ativo=True)
        grupo6.save() 
        grupo7 = Grupo  (Numero=7, Nome='Grupo 7',   Ativo=False)
        grupo7.save() 
        grupo8 = Grupo  (Numero=8, Nome='Grupo 8',   Ativo=False)
        grupo8.save() 
        grupo9 = Grupo  (Numero=9, Nome='Grupo 9',   Ativo=False)
        grupo9.save() 
        grupo10 = Grupo (Numero=10, Nome='Grupo 10', Ativo=False)
        grupo10.save() 
        grupo11 = Grupo (Numero=11, Nome='Grupo 11', Ativo=False)
        grupo11.save() 
        grupo12 = Grupo (Numero=12, Nome='Grupo 12', Ativo=False)
        grupo12.save() 
        self.stdout.write (self.style.SUCCESS ('4. Tabela de Grupos refeita'))

        # Atribui grupos operadores:
        grupo1.GrupoOperador = grupo2
        grupo1.save() 
        grupo2.GrupoOperador = grupo3
        grupo2.save() 
        grupo3.GrupoOperador = grupo4
        grupo3.save() 
        grupo4.GrupoOperador = grupo5
        grupo4.save() 
        grupo5.GrupoOperador = grupo6
        grupo5.save() 
        grupo6.GrupoOperador = grupo1
        grupo6.save() 
        grupo7.GrupoOperador = grupo7
        grupo7.save() 
        grupo8.GrupoOperador = grupo8
        grupo8.save() 
        grupo9.GrupoOperador = grupo9
        grupo9.save() 
        grupo10.GrupoOperador = grupo10
        grupo10.save() 
        grupo11.GrupoOperador = grupo11
        grupo11.save() 
        grupo12.GrupoOperador = grupo12
        grupo12.save() 
        self.stdout.write (self.style.SUCCESS ('5. Grupos operadores atribuidos'))

        # Inicializa tabela de movimentos dos grupos:
        movi = Movimento (Grupo=grupo1,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo2,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo3,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo4,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo5,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo6,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo7,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo8,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo9,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo10, Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo11, Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        movi = Movimento (Grupo=grupo12, Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
        movi.save() 
        self.stdout.write (self.style.SUCCESS ('6. Tabela de Movimentos inicializada'))

        # Sorteia e grava novos valores:
        duracao = Controle.objects.filter (Nome='Ativo').first().Duracao
        for i in range (1, duracao+1):
            prazo, demanda = sortear()
            sorte = Sorteado (Dia=i, PrazoSorteado=prazo, DemandaSorteada=demanda)
            sorte.save ()
        self.stdout.write (self.style.SUCCESS ('7. Dados sorteados e gravados para {} dias'.format(duracao)))

        self.stdout.write (self.style.SUCCESS ('Banco de dados reinicializado como sucesso.'))

        prazoMedio   = Sorteado.objects.aggregate (Avg('PrazoSorteado'))   ['PrazoSorteado__avg']
        demandaMedia = Sorteado.objects.aggregate (Avg('DemandaSorteada')) ['DemandaSorteada__avg']
        self.stdout.write (self.style.SUCCESS ('Demanda média: {} unidades'.format(round(demandaMedia,2))))
        self.stdout.write (self.style.SUCCESS ('Prazo médio: {} dias'.format(round(prazoMedio,2))))
