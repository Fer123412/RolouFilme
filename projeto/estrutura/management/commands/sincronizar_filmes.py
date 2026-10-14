from django.core.management.base import BaseCommand
from estrutura.tmdb import sincronizar_populares

class Command(BaseCommand):
    help = "Importa filmes populares do TMDB"

    def handle(self, *args, **options):
        filmes = sincronizar_populares()
        self.stdout.write(self.style.SUCCESS(f"{len(filmes)} filmes importados com sucesso!"))