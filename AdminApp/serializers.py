from rest_framework import serializers
from AdminApp.models import Workstations, Users, Rooms, Sanitizations

class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstations
        fields = ('id',
                  'tag',{\n" +
                "        \"id\": 1,\n" +
                "        \"roomname\": \"lab1\",\n" +
                "        \"xroom\": 10,\n" +
                "        \"yroom\": 10,\n" +
                "        \"archived\": 0\n" +
                "    },\n" +
                "    {\n" +
                "        \"id\": 2,\n" +
                "        \"roomname\": \"lab2\",\n" +
                "        \"xroom\": 20,\n" +
                "        \"yroom\": 20,\n" +
                "        \"archived\": 0\n" +
                "    }
                  'workstationname',
                  'xworkstation',
                  'yworkstation',
                  'idroom',
                  'state',
                  'sanitized',
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

class SanitizaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanitizations
        fields = ('id',
                  'idworkstation',
                  'iduser',
                  'sanitizationtime')