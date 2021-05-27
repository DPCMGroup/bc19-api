from rest_framework import serializers
from AdminApp.models import Workstations, Users, Rooms, Sanitizations, Bookings, Attendances


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
                  'sanitized',
                  'archived')


class AttendencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendances
        fields = ('id',
                  'idbooking',
                  'starttime',
                  'endtime')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ('id',
                  'idworkstation',
                  'iduser',
                  'starttime',
                  'endtime')


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
                  'archived',
                  'unavailable')


class SanitizaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanitizations
        fields = ('id',
                  'idworkstation',
                  'iduser',
                  'sanitizationtime')
