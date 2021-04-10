from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Workstations, Users, Rooms, Bookings
from AdminApp.serializers import WorkstationSerializer, UserSerializer
from datetime import datetime
import json


# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def insertWorkstation(request):
    workstation_data = JSONParser().parse(request)
    workstations_serializer = WorkstationSerializer(data=workstation_data)
    if workstations_serializer.is_valid():
        workstations_serializer.save()
        return JsonResponse("Added Successfully!!", safe=False)
    return JsonResponse("Failed to Add.", safe=False)


@require_http_methods(["GET"])
def getWorkstations(request):
    workstations = Workstations.objects.all()
    workstations_serializer = WorkstationSerializer(workstations, many=True)
    return JsonResponse(workstations_serializer.data, safe=False)


@require_http_methods(["GET"])
def deleteWorkstation(request, id):
    if Workstations.objects.exists(id=id):
        workstation = Workstations.objects.get(id=id)
    else:
        return JsonResponse("No workstation found", safe=False)
    workstation.delete()
    return JsonResponse("Deleted Successfully!!", safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def getWorkstationStatus(request): #get id, nome, stato nome stanza e da chi e’ prenotata
    tag_data = JSONParser().parse(request)
    tag = tag_data['tag']
    dic = {}
    if not Workstations.objects.filter(tag=tag):
        return JsonResponse("Nessuna workstation trovata corrispondente al tag", safe=False)

    works = Workstations.objects.get(tag=tag)
    dic['workId'] = works.id
    dic['workName'] = works.workstationname
    dic['workStatus'] = works.state
    dic['roomName'] = works.idroom.roomname
    dic['bookedToday'] = 0

    bookings = Bookings.objects.filter(idworkstation=works.id, endtime__gte=datetime.now(), endtime__day=datetime.now().day)
    if bookings:
        bookArray = []
        for book in bookings:
            bookDic = {}
            bookDic['bookerId'] = book.iduser_id
            bookDic['bookerUsername'] = book.iduser.username
            bookDic['bookerName'] = book.iduser.name
            bookDic['bookerSurname'] = book.iduser.surname
            bookDic['from'] = book.starttime.strftime("%d/%m/%Y, %H:%M")
            bookDic['to'] = book.endtime.strftime("%d/%m/%Y, %H:%M")
            bookArray.append(bookDic)
        dic['bookedToday'] = 1
        dic['bookings'] = bookArray
    return JsonResponse(json.dumps(dic), safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def loginUser(request):
    user_data = JSONParser().parse(request)
    if Users.objects.exists(username=str(user_data['username']), password=str(user_data['password'])):
        loginuser = Users.objects.get(username=str(user_data['username']), password=str(user_data['password']))
        user_serializer = UserSerializer(loginuser, many=False)
        return JsonResponse(user_serializer.data, safe=False)
    else:
        return JsonResponse("No user found", safe=False)

@require_http_methods(["GET"])
def userBookings(request, userId): #data - orainizio - orafine - postazione - stanza
    bookings = Bookings.objects.filter(iduser=userId, endtime__gte=datetime.now())
    array = []
    for book in bookings:
        dic = {}
        dic['bookId'] = book.id
        dic['workId'] = book.idworkstation_id
        dic['workName'] = book.idworkstation.workstationname
        dic['roomId'] = book.idworkstation.idroom_id
        dic['roomName'] = book.idworkstation.idroom.roomname
        dic['start'] = book.starttime.strftime("%d/%m/%Y, %H:%M")
        dic['end'] = book.endtime.strftime("%d/%m/%Y, %H:%M")
        array.append(dic)
    return JsonResponse(json.dumps(array), safe=False)


