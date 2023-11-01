"""Test models."""
from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.db.models import ForeignKey
from rest_framework import serializers


class WeatherStation(models.Model):  # noqa
    number = models.IntegerField(unique=True)

    centroid = models.PointField(name='centroid', srid=4326)
    centroid_rd = models.PointField(name='centroid_rd', srid=28992)

    def __str__(self):  # noqa
        return 'DISPLAY FIELD CONTENT'


class TemperatureRecord(models.Model):  # noqa
    class Meta:  # noqa
        unique_together = ('station', 'date')

    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.DecimalField(decimal_places=3, max_digits=6)


class SimpleModel(models.Model):
    name = serializers.CharField(max_length=25)
    age = serializers.IntegerField()
    sign = serializers.CharField(max_length=25)


class Person(models.Model):
    name = serializers.CharField(max_length=255)


class Thing(models.Model):
    name = serializers.CharField(max_length=128)
    person = ForeignKey(Person, related_name='things', on_delete=models.DO_NOTHING)


class Location(models.Model):
    geometrie = PointField(srid=28992)
