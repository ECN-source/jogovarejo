from django.core.management.base import BaseCommand

from jogovarejo.models import Controle, Sorteado
from jogovarejo.sorteio import sortear

class Command (BaseCommand):
    help = "Sorteia novos valores e grava no banco de dados para novo jogo"

    def handle (self, *args, **options):
        Sorteado.objects.all().delete()
        self.stdout.write (self.style.SUCCESS ('Excluiu sorteio anterior'))
        
        duracao = Controle.objects.filter (Nome='Ativo').first().Duracao
        for i in range (1, duracao+1):
            prazo, demanda = sortear()
            sorte = Sorteado (Dia=i, PrazoSorteado=prazo, DemandaSorteada=demanda)
            sorte.save ()
        self.stdout.write (self.style.SUCCESS ('Gravados '+ str(duracao) +' novos valores'))
