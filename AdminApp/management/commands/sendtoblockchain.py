from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Invia informazioni alla blockchain'

    def handle(self, *args, **options):
        print("è stato chiamato il comando per inviare informazioni alla blockchain")