from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.serializers import BookingSerializer
from AdminApp.models import Bookings
from datetime import datetime, timedelta
from AdminApp.Views import errorCode


@require_http_methods(["POST"])
def getTimeUntilNextBooking(request):
    data = JSONParser().parse(request)
    # mi prendo tutte le prentoazioni di oggi della workstation
    time_now = datetime.now().replace(second=0, microsecond=0)
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
                return JsonResponse(-3, safe=False)
            # e' in corso una prenotazione di un altro utente
            return JsonResponse(-2, safe=False)
        else:
            # controllo che ci siano almeno 60 min da quella successiva
            next_book = today_bookings[0]
            difference = next_book.starttime - time_now
            diff = difference.total_seconds() / 60
            if diff < 60:
                # se mancano meno di 60 min dalla mia prenotazione, faccio partite l'occupazione
                if next_book.iduser_id == data['iduser']:
                    return JsonResponse(-3, safe=False)
                # troppo poco tempo, considero come occupato
                return JsonResponse(-2, safe=False)
            else:
                # inserisco la prenotazione e l'occupazione
                hour = diff // 60
                return JsonResponse(hour, safe=False)
    else:
        # non sono presente alcune prenotazioni nella giornata di oggi
        return JsonResponse(-1, safe=False)




@require_http_methods(["POST"])
def insertBooking(request):
    book_data = JSONParser().parse(request)
    bookings_serializer = BookingSerializer(data=book_data)
    if bookings_serializer.is_valid():
        bookings_serializer.save()
        return JsonResponse(errorCode.BOOK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.BOOK_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["POST"])
def modifyBooking(request):
    book_data = JSONParser().parse(request)
    if not Bookings.objects.filter(id=book_data['id']):
        return JsonResponse(errorCode.BOOK_THING + errorCode.NO_FOUND, safe=False)
    book = Bookings.objects.get(id=book_data['id'])
    bookings_serializer = BookingSerializer(book, data=book_data)
    if bookings_serializer.is_valid():
        bookings_serializer.save()
        return JsonResponse(errorCode.BOOK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.BOOK_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def deleteBooking(request, id):
    if Bookings.objects.filter(id=id):
        book = Bookings.objects.get(id=id)
        book.delete()
        return JsonResponse(errorCode.BOOK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.BOOK_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["GET"])
def getBookings(request):
    books = Bookings.objects.all()
    book_serializer = BookingSerializer(books, many=True)
    return JsonResponse(book_serializer.data, safe=False)
