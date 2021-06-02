from django.core.management.base import BaseCommand
from datetime import datetime
from AdminApp.models import Reports
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
            report = recurrentReport()
            if report['occupations'] or report['sanitizations']:
                csv_str = "idworkstation,iduser,username,name,surname,type,timestart,timend\n"
                for occupation in report['occupations']:
                    csv_str += str(occupation['idoccupation']) + "," + str(occupation['iduser']) + "," + occupation[
                        'username'] + "," + occupation['name'] + "," + occupation['surname'] + "," + str(
                        occupation['type']) + "," + occupation['starttime'] + "," + occupation['endtime'] + "\n"
                csv_str += ",,,,,,\n"
                csv_str += "idsanitize,iduser,username,name,surname,type,time\n"
                for sanitize in report['sanitizations']:
                    csv_str += str(sanitize['idsanitize']) + "," + str(sanitize['iduser']) + "," + sanitize['username'] + "," + \
                               sanitize['name'] + "," + sanitize['surname'] + "," + str(sanitize['type']) + "," + sanitize[
                                   'time'] + "\n"
                tx_hash = bl_client.hashAndSendStringData(csv_str)
                bl_client.startListening(tx_hash, self.txCompleteHandle, self.fail)
            sleep(320)


    def txCompleteHandle(self, tx_hash, data_hash):
        # inserisco nel db
        report = Reports.objects.create(reporttime=datetime.now().replace(second=0, microsecond=0), fileHash=data_hash,
                                        blockchainhash=tx_hash)
        print(datetime.now().strftime("%Y-%m-%d %H:%M") + "inserito report, id: " + str(report.id), flush=True)
        report.save()

    def fail(self):
        return
