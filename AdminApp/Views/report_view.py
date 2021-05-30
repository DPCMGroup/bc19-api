from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q
from AdminApp.models import Attendances, Bookings, Sanitizations
from datetime import datetime, timedelta
from AdminApp.Views import errorCode
