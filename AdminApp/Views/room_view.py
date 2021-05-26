from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Rooms, RoomsFailures, Workstations
from AdminApp.serializers import RoomSerializer
from AdminApp.Views import errorCode
from datetime import datetime
from django.db.models import Q


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
    for roomData in rooms_serializer.data:
        if roomData['unavailable'] == 1:
            roomData['isDataSet'] = 0
            failure = RoomsFailures.objects.filter(
                Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), idroom=roomData['id']).order_by('-starttime')
            if failure:
                roomData['isDataSet'] = 1
                roomData['failureFrom'] = failure[0].starttime.strftime("%Y-%m-%d %H:%M")
                roomData['failureTo'] = failure[0].endtime.strftime("%Y-%m-%d %H:%M") if failure[0].endtime else 0
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


@require_http_methods(["GET"])
def roomToSanitize(request):
    roomSet = set()
    dirty_workstations = Workstations.objects.filter(sanitized=0, archived=0)
    for workst in dirty_workstations:
        roomSet.add(workst.idroom_id)
    dirty_rooms = Rooms.objects.filter(id__in=roomSet)
    room_serializer = RoomSerializer(dirty_rooms, many=True)
    return JsonResponse(room_serializer.data, safe=False)
