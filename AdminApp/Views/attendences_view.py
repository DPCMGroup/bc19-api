from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q
from AdminApp.models import Attendances, Bookings, Workstations
from AdminApp.serializers import BookingSerializer, AttendencesSerializer, WorkstationSerializer
from datetime import datetime, timedelta
from AdminApp.Views import errorCode


@require_http_methods(["POST"])
def insertOccupation(request):
    data = JSONParser().parse(request)
    # mi prendo tutte le prentoazioni di oggi della workstation
    time_now = datetime.strptime(data['time'], "%Y-%m-%d %H:%M")
    today_max = time_now.replace(hour=23, minute=59, second=0, microsecond=0)
    today_bookings = Bookings.objects.filter(idworkstation=data['idworkstation'],
                                             endtime__range=(time_now, today_max)).order_by('starttime')
    # se sono presenti prenotazioni da adesso in poi
    if today_bookings:
        # verifico se e' in corso una prenotazione
        current_book = today_bookings.filter(starttime__lte=time_now, endtime__gte=time_now)
        if current_book:
            # controllo se e' l'utente stesso
            if current_book[0].iduser == data['iduser']:
                # inserisco l'occupazione fino alla fine della prenotazione
                return insertAttendence(data['idworkstation'], current_book[0].id, time_now, current_book[0].endtime)
            # e' in corso una prenotazione di un altro utente
            return JsonResponse(errorCode.BOOK_THING + errorCode.EXISTS, safe=False)
        else:
            # controllo che ci siano almeno 60 min da quella successiva
            next_book = today_bookings[0]
            difference = next_book.starttime - datetime.strptime(data['time'], "%Y-%m-%d %H:%M")
            if difference.total_seconds() / 60 < 60:
                # se mancano meno di 60 min dalla mia prenotazione, faccio partite l'occupazione
                if next_book.iduser == data['iduser']:
                    return insertAttendence(data['idworkstation'], next_book.id, time_now, next_book.endtime)
                # troppo poco tempo, considero come occupato
                return JsonResponse(errorCode.BOOK_THING + errorCode.EXISTS, safe=False)
            else:
                # inserisco la prenotazione e l'occupazione
                return insertBookingAndAttendence(idworkstation=data['idworkstation'], iduser=data['iduser'],
                                                  starttime=time_now,
                                                  endtime=next_book.endtime)
    else:
        # non sono presente alcune prenotazioni nella giornata di oggi
        return insertBookingAndAttendence(idworkstation=data['idworkstation'], iduser=data['iduser'],
                                          starttime=time_now, endtime=time_now.replace(hour=18, minute=0, second=0))


def insertAttendence(idworkstation, idbooking, starttime, endtime):
    attendences_serializer = AttendencesSerializer(idbooking=idbooking, starttime=starttime, endtime=endtime)
    if attendences_serializer.is_valid():
        attendences_serializer.save()
        workstation = Workstations.objects.get(id=idworkstation)
        workstation.state = 1
        workstation.sanitized = 0
        workstations_serializer = WorkstationSerializer(workstation)
        if workstations_serializer.is_valid():
            workstations_serializer.save()
            return JsonResponse(attendences_serializer.data, safe=False)
        return JsonResponse(errorCode.WORK_THING + errorCode.FAILURE, safe=False)
    return JsonResponse(errorCode.ATTENDENCES_THING + errorCode.FAILURE, safe=False)


def insertBookingAndAttendence(idworkstation, iduser, starttime, endtime):
    bookings_serializer = BookingSerializer(idworkstation=idworkstation, iduser=iduser, starttime=starttime,
                                            endtime=endtime)
    if bookings_serializer.is_valid():
        bookings_serializer.save()
        return insertAttendence(idworkstation, bookings_serializer.data['id'], starttime, endtime)
    return JsonResponse(errorCode.BOOK_THING + errorCode.FAILURE, safe=False)
