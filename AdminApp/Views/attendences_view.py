from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Attendances, Bookings, Workstations, Users
from datetime import datetime, timedelta
from AdminApp.Views import errorCode


@require_http_methods(["POST"])
def terminateOccupation(request):
    data = JSONParser().parse(request)
    time_now = datetime.strptime(data['time'], "%Y-%m-%d %H:%M")
    if not Attendances.objects.filter(id=data['idattendence']):
        return JsonResponse(errorCode.ATTENDENCES_THING + errorCode.NO_FOUND, safe=False)
    attendence = Attendances.objects.get(id=data['idattendence'])
    if time_now < attendence.endtime.replace(tzinfo=None):
        attendence.idbooking.endtime = time_now
        attendence.endtime = time_now
        attendence.idbooking.save()
    attendence.idbooking.idworkstation.state = 0
    attendence.idbooking.idworkstation.save()
    attendence.save()
    return JsonResponse(errorCode.ATTENDENCES_THING + errorCode.OK, safe=False)


@require_http_methods(["POST"])
def insertOccupation(request):
    data = JSONParser().parse(request)
    # mi prendo tutte le prentoazioni di oggi della workstation
    time_now = datetime.strptime(data['time'], "%Y-%m-%d %H:%M")
    time_to_add = data['hour']
    today_max = time_now.replace(hour=23, minute=59, second=0, microsecond=0)
    today_bookings = Bookings.objects.filter(idworkstation=data['idworkstation'],
                                             endtime__range=(time_now, today_max)).order_by('starttime')
    # se sono presenti prenotazioni da adesso in poi
    if today_bookings:
        # verifico se e' in corso una prenotazione
        current_book = today_bookings.filter(starttime__lte=time_now, endtime__gte=time_now)
        if current_book:
            # controllo se e' l'utente stesso
            if current_book[0].iduser_id == data['iduser']:
                # inserisco l'occupazione fino alla fine della prenotazione
                return insertAttendence(data['idworkstation'], current_book[0], time_now, current_book[0].endtime)
            # e' in corso una prenotazione di un altro utente
            return JsonResponse(errorCode.BOOK_THING + errorCode.EXISTS, safe=False)
        else:
            # controllo che ci siano almeno 60 min da quella successiva
            next_book = today_bookings[0]
            difference = next_book.starttime.replace(tzinfo=None) - datetime.strptime(data['time'],
                                                                                      "%Y-%m-%d %H:%M").replace(
                tzinfo=None)
            if difference.total_seconds() / 60 < 60:
                # se mancano meno di 60 min dalla mia prenotazione, faccio partite l'occupazione
                if next_book.iduser_id == data['iduser']:
                    next_book.starttime = time_now
                    next_book.save()
                    return insertAttendence(data['idworkstation'], next_book, time_now, next_book.endtime)
                # troppo poco tempo, considero come occupato
                return JsonResponse(errorCode.BOOK_THING + errorCode.EXISTS, safe=False)
            else:
                # inserisco la prenotazione e l'occupazione
                endtime_refactor = time_now + timedelta(hours=time_to_add)
                if time_to_add == 0:
                    return insertBookingAndAttendence(idworkstation=data['idworkstation'], iduser=data['iduser'],
                                                      starttime=time_now,
                                                      endtime=next_book.starttime - timedelta(minutes=15))
                else:
                    endtime_refactor = endtime_refactor if endtime_refactor < next_book.starttime - timedelta(
                        minutes=15) else next_book.starttime - timedelta(minutes=15)
                    return insertBookingAndAttendence(idworkstation=data['idworkstation'], iduser=data['iduser'],
                                                      starttime=time_now, endtime=endtime_refactor)

    else:
        # non sono presente alcune prenotazioni nella giornata di oggi
        endtime_refactor = time_now.replace(hour=23, minute=0, second=0) if time_to_add == 0 else time_now + timedelta(
            hours=time_to_add)
        return insertBookingAndAttendence(idworkstation=data['idworkstation'], iduser=data['iduser'],
                                          starttime=time_now, endtime=endtime_refactor)


def insertAttendence(idworkstation, booking, starttime, endtime):
    if not Workstations.objects.filter(id=idworkstation):
        JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)
    attendence, create = Attendances.objects.get_or_create(idbooking=booking, starttime=starttime, endtime=endtime)
    workstation = Workstations.objects.get(id=idworkstation)
    dic = {'idattendence': attendence.id, 'idbooking': attendence.idbooking_id,
           'starttime': attendence.starttime.strftime("%Y-%m-%d %H:%M"),
           'endtime': attendence.endtime.strftime("%Y-%m-%d %H:%M")}
    workstation.state = 1
    workstation.sanitized = 0
    workstation.save()
    return JsonResponse(dic, safe=False)


def insertBookingAndAttendence(idworkstation, iduser, starttime, endtime):
    if not Workstations.objects.filter(id=idworkstation):
        JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)
    if not Users.objects.filter(id=iduser):
        JsonResponse(errorCode.USER_THING + errorCode.NO_FOUND, safe=False)
    user = Users.objects.get(id=iduser)
    workstation = Workstations.objects.get(id=idworkstation)
    booking = Bookings.objects.create(idworkstation=workstation, iduser=user, starttime=starttime,
                                      endtime=endtime)
    try:
        booking.save()
        return insertAttendence(idworkstation, booking, starttime, endtime)
    except:
        return JsonResponse(errorCode.BOOK_THING + errorCode.FAILURE, safe=False)
