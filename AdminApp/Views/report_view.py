from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.cron import createOccupationReport, createSanificationReport


@require_http_methods(["POST"])
def getOccupationReport(request):
    data = JSONParser().parse(request)
    return JsonResponse(createOccupationReport(data['starttime'].strftime("%Y-%m-%d %H:%M"),
                                               data['endtime'].strftime("%Y-%m-%d %H:%M")))


@require_http_methods(["POST"])
def getSanitizationReport(request):
    data = JSONParser().parse(request)
    return JsonResponse(createSanificationReport(data['starttime'].strftime("%Y-%m-%d %H:%M"),
                                                 data['endtime'].strftime("%Y-%m-%d %H:%M")))
