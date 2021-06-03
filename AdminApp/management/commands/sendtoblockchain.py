from django.core.management.base import BaseCommand
from datetime import datetime
from AdminApp.cron import recurrentReport
from web3pkg.BlockchainClient import Client
from time import sleep


class Command(BaseCommand):
    help = 'Invia informazioni alla blockchain'

    def handle(self, *args, **options):
        while True:
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": chiamato il comando per inviare informazioni alla blockchain",
                  flush=True)
            bl_client = Client()
            time_now = datetime.now()
            if time_now.hour == 23 and time_now.minute == 58:
                report = recurrentReport()
                if report['occupations'] or report['sanitizations']:
                    csv_str = "idoccupation,idworkstation,iduser,username,name,surname,type,timestart,timend\n"
                    for occupation in report['occupations']:
                        csv_str += str(occupation['idoccupation']) + "," + str(occupation['idworkstation']) + "," + str(
                            occupation['iduser']) + "," + occupation['username'] + "," + occupation['name'] + "," + \
                                   occupation['surname'] + "," + str(occupation['type']) + "," + occupation[
                                       'starttime'] + "," + occupation['endtime'] + "\n"
                    csv_str += ",,,,,,\n"
                    csv_str += "idsanitize,idworkstation,iduser,username,name,surname,type,time\n"
                    for sanitize in report['sanitizations']:
                        csv_str += str(sanitize['idsanitize']) + "," + str(sanitize['idworkstation']) + "," + str(
                            sanitize['iduser']) + "," + sanitize['username'] + "," + sanitize['name'] + "," + sanitize[
                                       'surname'] + "," + str(sanitize['type']) + "," + sanitize['time'] + "\n"
                    tx_hash = bl_client.hashAndSendStringData(csv_str)
                    bl_client.startListening(tx_hash)
            sleep(60)
