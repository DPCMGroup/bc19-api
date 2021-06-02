from AdminApp.models import WorkstationsFailures, RoomsFailures, Bookings, Reports, Attendances, Sanitizations
from datetime import datetime
from django.db.models import Q

def fail(self):
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + " fail", flush=True)

def txCompleteHandle(tx_hash, data_hash):
    # inserisco nel db
    report = Reports.objects.create(reporttime=datetime.now().replace(second=0, microsecond=0), fileHash=data_hash,
                                    blockchainhash=tx_hash)
    print(datetime.now().strftime("%Y-%m-%d %H:%M") + " inserito report, id: " + str(report.id), flush=True)
    report.save()

def recurrentReport():
    # prendo i report di oggi in ordine desc
    time_now = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    time_midnight = time_now.replace(hour=0, minute=0, second=0, microsecond=0)
    dic = {}
    dic['occupations'] = createOccupationReport(time_midnight, time_now)
    dic['sanitizations'] = createSanificationReport(time_midnight, time_now)
    return dic


def createOccupationReport(starttime, endtime):
    report_occupation = Attendances.objects.filter(
        Q(endtime__gte=starttime, endtime__lte=endtime) | Q(starttime__gte=starttime, starttime__lte=endtime))
    reportArray = []
    for occupation in report_occupation:
        dic = {}
        dic['idoccupation'] = occupation.id
        dic['idworkstation'] = occupation.idbooking.idworkstation.id
        dic['iduser'] = occupation.idbooking.iduser.id
        dic['username'] = occupation.idbooking.iduser.username
        dic['name'] = occupation.idbooking.iduser.name
        dic['surname'] = occupation.idbooking.iduser.surname
        dic['type'] = occupation.idbooking.iduser.type
        dic['starttime'] = occupation.starttime.strftime("%Y-%m-%d %H:%M")
        dic['endtime'] = occupation.endtime.strftime("%Y-%m-%d %H:%M")
        reportArray.append(dic)
    return reportArray


def createSanificationReport(starttime, endtime):
    report_sanification = Sanitizations.objects.filter(sanitizationtime__gte=starttime, sanitizationtime__lte=endtime)
    reportArray = []
    for sanification in report_sanification:
        dic = {}
        dic['idsanitize'] = sanification.id
        dic['idworkstation'] = sanification.idworkstation.id
        dic['iduser'] = sanification.iduser.id
        dic['username'] = sanification.iduser.username
        dic['name'] = sanification.iduser.name
        dic['surname'] = sanification.iduser.surname
        dic['type'] = sanification.iduser.type
        dic['time'] = sanification.sanitizationtime.strftime("%Y-%m-%d %H:%M")
        reportArray.append(dic)
    return reportArray


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
