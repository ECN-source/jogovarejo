from django.core.management.base import BaseCommand

from jogovarejo.models import Grupo, Movimento, Compra
from jogovarejo.dinamica import ProcessaUmDia


class Command (BaseCommand):
    help = "Reinicia movimentos do jogo preservando demais tabelas inclusive o sorteio"

    def handle (self, *args, **options):

        grGerente = Grupo.objects.get (Numero=1)
        for i in range(1, 41, 2):
            mensagem = ProcessaUmDia (grGerente, 65)
            mensagem = ProcessaUmDia (grGerente,  0)
