from AdminApp.models import WorkstationsFailures, RoomsFailures, Bookings
from datetime import datetime
from django.db.models import Q


def checkdatabase():
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + ": chiamato il comando per controllare il database",
          flush=True)
    # controllo lo stato inizio failure
    workstationFailureStartList = WorkstationsFailures.objects.filter(
        Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), archived=0)
    for workFail in workstationFailureStartList:
        if workFail.starttime.replace(tzinfo=None) <= datetime.now() and workFail.idworkstation.state != 3:
            workFail.idworkstation.state = 3
            workFail.idworkstation.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": impostato stato fail della postazione, idworkstation:" + str(
                workFail.idworkstation.id), flush=True)
    roomFailureStartList = RoomsFailures.objects.filter(
        Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), archived=0)
    for roomFail in roomFailureStartList:
        if roomFail.starttime.replace(tzinfo=None) <= datetime.now() and roomFail.idroom.unavailable == 0:
            roomFail.idroom.unavailable = 1
            roomFail.idroom.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": impostato stato fail della stanza, idroom:" + str(roomFail.idroom.id),
                  flush=True)

    # controllo lo stato fine failure
    workstationFailureStopList = WorkstationsFailures.objects.filter(endtime__lte=datetime.now(), archived=0)
    for workFail in workstationFailureStopList:
        if workFail.idworkstation.state == 3:
            workFail.idworkstation.state = 0
            workFail.idworkstation.save()
            workFail.archived = 1
            workFail.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": modificato stato fine failure della postazione, idworkstation:" + str(
                workFail.idworkstation.id), flush=True)
        workFail.archived = 1
        workFail.save()
    roomFailureStopList = RoomsFailures.objects.filter(endtime__lte=datetime.now(), archived=0)
    for roomFail in roomFailureStopList:
        if roomFail.idroom.unavailable == 1:
            roomFail.idroom.unavailable = 0
            roomFail.idroom.save()
            roomFail.archived = 1
            roomFail.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": modificato stato fine failure della stanza, idroom:" + str(
                roomFail.idroom.id), flush=True)
        roomFail.archived = 1
        roomFail.save()

    # controllo lo stato fine booking
    booksEnd = Bookings.objects.filter(endtime__lte=datetime.now(), archived=0)
    for book in booksEnd:
        if book.idworkstation.state != 0 and book.idworkstation.state != 3:
            book.idworkstation.state = 0
            book.idworkstation.save()
            book.archived = 1
            book.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": modificato stato della postazione per fine booking, idworkstation:" + str(
                book.idworkstation.id), flush=True)

    # controllo lo stato inizio booking
    booksStart = Bookings.objects.filter(endtime__gte=datetime.now(), archived=0)
    for book in booksStart:
        if book.starttime.replace(tzinfo=None) <= datetime.now() and book.idworkstation.state == 0:
            book.idworkstation.state = 2
            book.idworkstation.save()
            print(datetime.now().strftime(
                "%Y-%m-%d %H:%M") + ": modificato stato della postazione per inizio booking, idworkstation:" + str(
                book.idworkstation.id), flush=True)
