from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Rooms
from AdminApp.serializers import RoomSerializer
import AdminApp.Views.errorCode as errorCode

@require_http_methods(["POST"])
def insertRoom(request):
    room_data = JSONParser().parse(request)
    room_serializer = RoomSerializer(data=room_data)
    if room_serializer.is_valid():
        room_serializer.save()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def getRooms(request):
    rooms = Rooms.objects.all()
    rooms_serializer = RoomSerializer(rooms, many=True)
    return JsonResponse(rooms_serializer.data, safe=False)


@require_http_methods(["POST"])
def modifyRoom(request):
    room_data = JSONParser().parse(request)
    if not Rooms.objects.filter(id=room_data['id']):
        return JsonResponse(errorCode.ROOM_THING + errorCode.NO_FOUND, safe=False)
    room = Rooms.objects.get(id=room_data['id'])
    room_serializer = RoomSerializer(room, data=room_data)
    if room_serializer.is_valid():
        room_serializer.save()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def deleteRoom(request, id):
    if Rooms.objects.filter(id=id):
        room = Rooms.objects.get(id=id)
        room.delete()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.NO_FOUND, safe=False)
