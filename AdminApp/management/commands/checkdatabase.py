from django.core.management.base import BaseCommand
from AdminApp.models import WorkstationsFailures, RoomsFailures, Bookings
from datetime import datetime
from django.db.models import Q


class Command(BaseCommand):
    help = 'Fa un controllo nel database aggiornando gli stati delle postazioni o stanze'

    def handle(self, *args, **options):
        print("è stato chiamato il comando per controllare il database")
        # controllo lo stato inizio failure
        workstationFailureStartList = WorkstationsFailures.objects.filter(
            Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), archived=0)
        for workFail in workstationFailureStartList:
            if workFail.starttime.replace(tzinfo=None) <= datetime.now() and workFail.idworkstation.state != 3:
                workFail.idworkstation.state = 3
                workFail.idworkstation.save()
        roomFailureStartList = RoomsFailures.objects.filter(
            Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), archived=0)
        for roomFail in roomFailureStartList:
            if roomFail.starttime.replace(tzinfo=None) <= datetime.now() and roomFail.idroom.unavailable == 0:
                roomFail.idroom.unavailable = 1
                roomFail.idroom.save()

        # controllo lo stato fine failure
        workstationFailureStopList = WorkstationsFailures.objects.filter(endtime__lte=datetime.now(), archived=0)
        for workFail in workstationFailureStopList:
            if workFail.idworkstation.state == 3:
                workFail.idworkstation.state = 0
                workFail.idworkstation.save()
            workFail.archived = 1
            workFail.save()
        roomFailureStopList = RoomsFailures.objects.filter(endtime__lte=datetime.now(), archived=0)
        for roomFail in roomFailureStopList:
            if roomFail.idroom.unavailable == 1:
                roomFail.idroom.unavailable = 0
                roomFail.idroom.save()
            roomFail.archived = 1
            roomFail.save()

        # controllo lo stato fine booking
        booksEnd = Bookings.objects.filter(endtime__lte=datetime.now(), archived=0)
        for book in booksEnd:
            if book.idworkstation.state == 2:
                book.idworkstation.state = 0
                book.idworkstation.save()

        # controllo lo stato inizio booking
        booksStart = Bookings.objects.filter(endtime__gte=datetime.now(), archived=0)
        for book in booksStart:
            if book.starttime.replace(tzinfo=None) <= datetime.now():
                book.idworkstation.state = 2
                book.idworkstation.save()
