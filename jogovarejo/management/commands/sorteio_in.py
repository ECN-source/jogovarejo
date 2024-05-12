from django.core.management.base import BaseCommand
from django.db import IntegrityError
import csv

from jogovarejo.models import Sorteado


class Command (BaseCommand):
    help = "Importa sorteio para Jogo Varejo do arquivo 'sorteio_in.csv'"

    def handle (self, *args, **options):

        with open ('sorteio_in.csv', encoding='utf-8', newline='') as arq:
            with open ('sorteio_err.csv', 'w', encoding='utf-8', newline='') as arqErr:
                # Zera conteúdo da tabela "Sorteado":
                Sorteado.objects.all().delete()
                tab    = csv.reader (arq,    delimiter=';')
                tabErr = csv.writer (arqErr, delimiter=';')
                linImportadas = 0
                linRejeitadas = 0
                lintotal      = 0
                for lin in tab:
                    try:
                        sorte = Sorteado (Dia=lin[0], PrazoSorteado=lin[1], DemandaSorteada=lin[2])
                        sorte.save ()
                        self.stdout.write (self.style.SUCCESS ('Importando sorteio do dia "%s"' % sorte.Dia))
                        linImportadas += 1
                        lintotal      += 1
                    except (IntegrityError):
                        tabErr.writerow (lin)
                        linRejeitadas += 1
                        lintotal      += 1
                        self.stdout.write (self.style.SUCCESS ('Rejeitou linha "%s"' % lintotal))
                arq.close ()
                arqErr.close () 
                self.stdout.write (self.style.SUCCESS ('Importou "%s" registros' % linImportadas))
                self.stdout.write (self.style.SUCCESS ('Rejeitou "%s" registros' % linRejeitadas))

