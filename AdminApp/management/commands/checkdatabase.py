from django.core.management.base import BaseCommand
from AdminApp.cron import checkdatabase


class Command(BaseCommand):
    help = 'Fa un controllo nel database aggiornando gli stati delle postazioni o stanze'

    def handle(self, *args, **options):
        checkdatabase()
