from rest_framework import serializers
from AdminApp.models import Workstations, Users, Rooms

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstations
        fields = ('id',
                  'tag',
                  'workstationname',
                  'xworkstation',
                  'yworkstation',
                  'idroom',
                  'state',
                  'archived')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id',
                  'username',
                  'password',
                  'name',
                  'surname',
                  'mail',
                  'type',
                  'archived')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ('id',
                  'roomname',
                  'xroom',
                  'yroom',
                  'archived')