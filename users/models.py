from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Zip(models.Model):
    zip = models.CharField(max_length=5)
    lat = models.FloatField()
    lng = models.FloatField()


class EventType(models.Model):
    event = models.CharField(max_length=100)

    def __str__(self):
        return self.event


class Region(models.Model):
    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.region


class State(models.Model):
    state = models.CharField(max_length=2)

    def __str__(self):
        return self.state


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zip = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    region = models.ManyToManyField(Region, blank=True)
    states = models.ManyToManyField(State, blank=True)
    event = models.ManyToManyField(EventType, blank=False)
    dstr_cad = models.CharField(max_length=20, blank=True)
    dstr_day = models.CharField(max_length=100, blank=True)
    distrib = models.BooleanField(null=False, default=True)
    q_string = models.CharField(max_length=1000, null=True)
    run_date = models.DateField(blank=True)
    run_date = models.DateField(blank=True, default=datetime(2050, 1, 1, 1, 00))

    def __str__(self):
        return f"{self.user.username} Profile"

