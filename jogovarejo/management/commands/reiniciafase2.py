from django.core.management.base import BaseCommand

from jogovarejo.models import Grupo, Movimento, Compra


class Command (BaseCommand):
    help = "Reinicia movimentos do jogo preservando demais tabelas inclusive o sorteio"

    def handle (self, *args, **options):

        # Zera conteúdo do banco de dados:
        Compra.objects.all().delete()
        Movimento.objects.all().delete()
        self.stdout.write (self.style.SUCCESS ('1 Zera tabela de movimentos e de compras'))
        
        # Acerta tabela de grupos para reiniciar Fase 2:
        grupos = Grupo.objects.all()
        for grupo in grupos:
            grupo.Fase1Ok = True
            grupo.Fase2Ok = False
            grupo.save() 
        self.stdout.write (self.style.SUCCESS ('2 Acertou tabela de grupos para reiniciar Fase 2'))

        # Inicializa tabela de movimentos dos grupos:
        grupos = Grupo.objects.all()
        for grupo in grupos:
            movi = Movimento (Grupo=grupo,  Dia=1, Recebido=0, AReceber=0, SaldoInicial=80)
            movi.save() 
        self.stdout.write (self.style.SUCCESS ('3 Tabela de Movimentos inicializada'))
