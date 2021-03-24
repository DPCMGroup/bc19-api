from rest_framework import serializers
from AdminApp.models import Workstation

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstation
        fields = ('WorkstationId',
                  'Xposition',
                  'Yposition',
                  'Status')