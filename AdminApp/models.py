# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Attendances(models.Model):
    idbooking = models.OneToOneField('Bookings', models.DO_NOTHING, db_column='idBooking')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attendances'


class Bookings(models.Model):
    idworkstation = models.ForeignKey('Workstations', models.DO_NOTHING, db_column='idWorkStation')  # Field name made lowercase.
    iduser = models.ForeignKey('Users', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime')  # Field name made lowercase.
    archived = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'bookings'


class WorkstationsFailures(models.Model):
    idworkstation = models.ForeignKey('Workstations', models.DO_NOTHING, db_column='idWorkStation')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    archived = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'workStationsFailures'

class RoomsFailures(models.Model):
    idroom = models.ForeignKey('Rooms', models.DO_NOTHING, db_column='idRoom')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    archived = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'roomsFailures'


class Reports(models.Model):
    reporttime = models.DateTimeField(db_column='reportTime', unique=True)  # Field name made lowercase.
    blockchainhash = models.CharField(db_column='blockchainHash', max_length=255)
    fileHash = models.CharField(db_column='fileHash', max_length=255)

    class Meta:
        managed = False
        db_table = 'reports'


class Rooms(models.Model):
    roomname = models.CharField(db_column='roomName', unique=True, max_length=20)  # Field name made lowercase.
    xroom = models.PositiveSmallIntegerField(db_column='xRoom')  # Field name made lowercase.
    yroom = models.PositiveSmallIntegerField(db_column='yRoom')  # Field name made lowercase.
    archived = models.IntegerField()
    unavailable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rooms'


class Sanitizations(models.Model):
    idworkstation = models.ForeignKey('Workstations', models.DO_NOTHING, db_column='idWorkStation')  # Field name made lowercase.
    iduser = models.ForeignKey('Users', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.
    sanitizationtime = models.DateTimeField(db_column='sanitizationTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sanitizations'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    mail = models.CharField(max_length=127)
    type = models.PositiveIntegerField()
    archived = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'


class Workstations(models.Model):
    workstationname = models.CharField(db_column='workStationName', unique=True, max_length=20)  # Field name made lowercase.
    tag = models.CharField(unique=True, max_length=20)  # Field name made lowercase.
    xworkstation = models.PositiveSmallIntegerField(db_column='xWorkStation')  # Field name made lowercase.
    yworkstation = models.PositiveSmallIntegerField(db_column='yWorkStation')  # Field name made lowercase.
    idroom = models.ForeignKey(Rooms, models.DO_NOTHING, db_column='idRoom')  # Field name made lowercase.
    state = models.PositiveIntegerField()
    sanitized = models.PositiveIntegerField()
    archived = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'workStations'
        unique_together = (('xworkstation', 'yworkstation', 'idroom'),)
