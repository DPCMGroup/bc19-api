from builtins import id

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AdminApp.models import Workstations, Users
from AdminApp.serializers import WorkstationSerializer, UserSerializer


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
    workstations = Workstations.objects.all()
    workstations_serializer = WorkstationSerializer(workstations, many=True)
    return JsonResponse(workstations_serializer.data, safe=False)


@csrf_exempt
def deleteWorkstation(request, id):
    try:
        workstation = Workstations.objects.get(state=0)
    except:
        return JsonResponse("No workstation found", safe=False)
    workstation.delete()
    return JsonResponse("Deleted Successfully!!", safe=False)

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            loginuser = Users.objects.get(username=str(user_data['username']), password=str(user_data['password']))
            user_serializer = UserSerializer(loginuser, many=False)
            return JsonResponse(user_serializer.data, safe=False)
        except:
            return JsonResponse("No user found", safe=False)




