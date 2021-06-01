from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Bookings, Users
from AdminApp.serializers import UserSerializer
from datetime import datetime
from AdminApp.Views import errorCode


@require_http_methods(["POST"])
def insertUser(request):
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(errorCode.USER_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.USER_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def getUsers(request):
    users = Users.objects.all()
    user_serializer = UserSerializer(users, many=True)
    return JsonResponse(user_serializer.data, safe=False)


@require_http_methods(["POST"])
def modifyUser(request):
    user_data = JSONParser().parse(request)
    if not Users.objects.filter(id=user_data['id']):
        return JsonResponse(errorCode.USER_THING + errorCode.NO_FOUND, safe=False)
    user = Users.objects.get(id=user_data['id'])
    user_serializer = UserSerializer(user, data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(errorCode.USER_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.USER_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def deleteUser(request, id):
    if Users.objects.filter(id=id):
        user = Users.objects.get(id=id)
        user.archived = 1
        user.save()
        return JsonResponse(errorCode.USER_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.USER_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["POST"])
def loginUser(request):
    user_data = JSONParser().parse(request)
    if Users.objects.filter(username=str(user_data['username']), password=str(user_data['password'])):
        loginuser = Users.objects.get(username=str(user_data['username']), password=str(user_data['password']))
        if loginuser.archived:
            return JsonResponse(errorCode.USER_THING + errorCode.ARCHIVED, safe=False)
        user_serializer = UserSerializer(loginuser, many=False)
        return JsonResponse(user_serializer.data, safe=False)
    else:
        return JsonResponse(errorCode.USER_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["GET"])
def userBookings(request, userId):
    bookings = Bookings.objects.filter(iduser=userId, endtime__gte=datetime.now())
    array = []
    for book in bookings:
        dic = {}
        dic['bookId'] = book.id
        dic['workId'] = book.idworkstation_id
        dic['workName'] = book.idworkstation.workstationname
        dic['roomId'] = book.idworkstation.idroom_id
        dic['roomName'] = book.idworkstation.idroom.roomname
        dic['start'] = book.starttime.strftime("%Y-%m-%d %H:%M")
        dic['end'] = book.endtime.strftime("%Y-%m-%d %H:%M")
        array.append(dic)
    return JsonResponse(array, safe=False)
