from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q
from AdminApp.models import Workstations, Bookings, Sanitizations, Users, WorkstationsFailures
from AdminApp.serializers import WorkstationSerializer
from datetime import datetime
from AdminApp.Views import errorCode


@require_http_methods(["POST"])
def insertWorkstation(request):
    workstation_data = JSONParser().parse(request)
    workstations_serializer = WorkstationSerializer(data=workstation_data)
    if workstations_serializer.is_valid():
        workstations_serializer.save()
        return JsonResponse(errorCode.WORK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.WORK_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def getWorkstations(request):
    workstations = Workstations.objects.all()
    workstations_serializer = WorkstationSerializer(workstations, many=True)
    for workData in workstations_serializer.data:
        if workData['state'] == 3:
            workData['isDataSet'] = 0
            failure = WorkstationsFailures.objects.filter(
                Q(endtime__gte=datetime.now()) | Q(endtime__isnull=True), idworkstation=workData['id']).order_by('-starttime')
            if failure:
                workData['isDataSet'] = 1
                workData['failureFrom'] = failure[0].starttime.strftime("%Y-%m-%d %H:%M")
                workData['failureTo'] = failure[0].endtime.strftime("%Y-%m-%d %H:%M") if failure[0].endtime else 0

    return JsonResponse(workstations_serializer.data, safe=False)


@require_http_methods(["POST"])
def modifyWorkstation(request):
    workstation_data = JSONParser().parse(request)
    if not Workstations.objects.filter(id=workstation_data['id']):
        return JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)
    workstation = Workstations.objects.get(id=workstation_data['id'])
    workstations_serializer = WorkstationSerializer(workstation, data=workstation_data)
    if workstations_serializer.is_valid():
        workstations_serializer.save()
        return JsonResponse(errorCode.WORK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.WORK_THING + errorCode.FAILURE, safe=False)


@require_http_methods(["GET"])
def deleteWorkstation(request, id):
    if Workstations.objects.filter(id=id):
        workstation = Workstations.objects.get(id=id)
        workstation.delete()
        return JsonResponse(errorCode.WORK_THING + errorCode.OK, safe=False)
    return JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)


@require_http_methods(["POST"])
def getWorkstationStatus(request):
    tag_data = JSONParser().parse(request)
    tag = tag_data['tag']
    dic = {}
    if not Workstations.objects.filter(tag=tag):
        return JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)

    works = Workstations.objects.get(tag=tag)
    dic['workId'] = works.id
    dic['workName'] = works.workstationname
    dic['workStatus'] = works.state
    dic['workSanitized'] = works.sanitized
    dic['roomName'] = works.idroom.roomname
    dic['bookedToday'] = 0

    bookings = Bookings.objects.filter(idworkstation=works.id, endtime__gte=datetime.now(),
                                       endtime__day=datetime.now().day).order_by('-endtime')
    if bookings:
        bookArray = []
        for book in bookings:
            bookDic = {}
            bookDic['bookerId'] = book.iduser_id
            bookDic['bookerUsername'] = book.iduser.username
            bookDic['bookerName'] = book.iduser.name
            bookDic['bookerSurname'] = book.iduser.surname
            bookDic['from'] = book.starttime.strftime("%Y-%m-%d %H:%M")
            bookDic['to'] = book.endtime.strftime("%Y-%m-%d %H:%M")
            bookArray.append(bookDic)
        dic['bookedToday'] = 1
        dic['bookings'] = bookArray

    return JsonResponse(dic, safe=False)


@require_http_methods(["POST"])
def sanizieWorkstation(request):
    data = JSONParser().parse(request)
    if not Workstations.objects.filter(tag=data['tag']):
        return JsonResponse(errorCode.WORK_THING + errorCode.NO_FOUND, safe=False)
    if not Users.objects.filter(id=data['idUser']):
        return JsonResponse(errorCode.USER_THING + errorCode.NO_FOUND, safe=False)
    user = Users.objects.get(id=data['idUser'])
    workstation = Workstations.objects.get(tag=data['tag'])
    sanitize = Sanitizations.objects.create(idworkstation=workstation, iduser=user, sanitizationtime=data['data'])
    workstation.sanitized = 1
    sanitize.save()
    workstation.save()
    return JsonResponse(errorCode.WORK_THING + errorCode.OK, safe=False)

@require_http_methods(["GET"])
def workstationToSanitize(request):
    dirty_workstations = Workstations.objects.filter(sanitized=0, archived=0)
    workstation_serializer = WorkstationSerializer(dirty_workstations, many=True)
    return JsonResponse(workstation_serializer.data, safe=False)