from rest_framework import serializers
from AdminApp.models import Workstations

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstations
        fields = ('workstationname',
                  'xworkstation',
                  'yworkstation',
                  'idroom',
                  'state',
                  'archived')