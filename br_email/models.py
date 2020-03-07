from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    EventName = models.CharField(max_length=500, blank=True, null=True)
    EventCity = models.CharField(max_length=50, blank=True, null=True)
    EventState = models.CharField(max_length=50, blank=True, null=True)
    EventUrl = models.CharField(max_length=1000, blank=True, null=True)
    EventTypes = models.CharField(max_length=500, blank=True, null=True)
    EventDate = models.DateTimeField(blank=True, null=True)
    RegCloseDate = models.DateTimeField(blank=True, null=True)
    Latitude = models.FloatField(blank=True, null=True)
    Longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Event'
