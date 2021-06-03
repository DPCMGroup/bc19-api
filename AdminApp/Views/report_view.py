from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AdminApp.models import Reports
from AdminApp.serializers import ReportSerializer
from AdminApp.cron import createOccupationReport, createSanificationReport


@require_http_methods(["POST"])
def getOccupationReport(request):
    data = JSONParser().parse(request)
    return JsonResponse(createOccupationReport(data['starttime'], data['endtime']), safe=False)


@require_http_methods(["POST"])
def getSanitizationReport(request):
    data = JSONParser().parse(request)
    return JsonResponse(createSanificationReport(data['starttime'], data['endtime']), safe=False)

@require_http_methods(["GET"])
def getReports(request):
    reports = Reports.objects.all()
    reports_serializer = ReportSerializer(reports, many=True)
    return JsonResponse(reports_serializer.data, safe=False)
