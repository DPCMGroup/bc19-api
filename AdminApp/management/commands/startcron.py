from django.core.management.base import BaseCommand
from AdminApp.cron import checkdatabase
from time import sleep


class Command(BaseCommand):
    help = 'esegue i jobs richiesti'

    def handle(self, *args, **options):
        while True:
            checkdatabase()
            sleep(60)
