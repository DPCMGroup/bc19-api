from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Rooms, RoomsFailures
from AdminApp.serializers import RoomSerializer, RoomFailureSerializer
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
                roomData['failureFrom'] = failure[0].starttime.strftime("%d/%m/%Y %H:%M")
                roomData['failureTo'] = failure[0].endtime.strftime("%d/%m/%Y %H:%M") if failure[0].endtime else 0
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


@require_http_methods(["POST"])
def insertRoomFailure(request):
    failure_data = JSONParser().parse(request)
    failure_serializer = RoomFailureSerializer(data=failure_data)
    print(failure_data)
    if failure_serializer.is_valid():
        failure_serializer.save()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["POST"])
def modifyRoomFailure(request):
    failure_data = JSONParser().parse(request)
    if not RoomsFailures.objects.filter(id=failure_data['id']):
        return JsonResponse(errorCode.ROOM_THING + errorCode.NO_FOUND, safe=False)
    failure = RoomsFailures.objects.get(id=failure_data['id'])
    failure_serializer = RoomFailureSerializer(failure, data=failure_data)
    if failure_serializer.is_valid():
        failure_serializer.save()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def deleteRoomFailure(request, id):
    if RoomsFailures.objects.filter(id=id):
        failure = RoomsFailures.objects.get(id=id)
        failure.delete()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["GET"])
def deleteRoomFailureByRoomId(request, roomid):
    if RoomsFailures.objects.filter(roomid=roomid):
        failure = RoomsFailures.objects.get(roomid=roomid)
        failure.delete()
        return JsonResponse(errorCode.ROOM_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.ROOM_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["GET"])
def getRoomsFailure(request):
    failures = RoomsFailures.objects.all()
    failure_serializer = RoomFailureSerializer(failures, many=True)
    return JsonResponse(failure_serializer.data, safe=False)
