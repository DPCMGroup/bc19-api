from rest_framework import serializers
from AdminApp.models import Workstations

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstations
        fields = ('workStationName',
                  'xWorkStation',
                  'yWorkStation',
                  'idRroom',
                  'state',
                  'archived')