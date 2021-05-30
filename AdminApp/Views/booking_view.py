from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.serializers import BookingSerializer
from AdminApp.models import Bookings
from datetime import datetime
from AdminApp.Views import errorCode


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
