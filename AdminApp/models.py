from django.db import models

# Create your models here.

class Workstation(models.Model):
    WorkstationId = models.IntegerField(primary_key=True)
    Xposition = models.IntegerField()
    Yposition = models.IntegerField()
    Status = models.CharField(max_length=100)