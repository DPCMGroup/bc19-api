from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AdminApp.models import Workstation
from AdminApp.serializers import WorkstationSerializer


# Create your views here.
@csrf_exempt
def insertWorkstation(request):
    if request.method == 'POST':
        workstation_data = JSONParser().parse(request)
        workstations_serializer = WorkstationSerializer(data=workstation_data)
        if workstations_serializer.is_valid():
            workstations_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Failed to Add.", safe=False)

    else:
        return JsonResponse("Wrong request method, required POST", safe=False)


@csrf_exempt
def getWorkstations(request):
    workstations = Workstation.objects.all()
    workstations_serializer = WorkstationSerializer(workstations, many=True)
    return JsonResponse(workstations_serializer.data, safe=False)


@csrf_exempt
def deleteWorkstation(request, id):
    try:
        workstation = Workstation.objects.get(WorkstationId=id)
    except:
        return JsonResponse("No object found", safe=False)
    workstation.delete()
    return JsonResponse("Deleted Successfully!!", safe=False)
