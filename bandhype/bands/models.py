from django.db import models
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField

class Band(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    percentage = models.FloatField()
    popularity = models.FloatField()
    time = models.DateField(auto_now_add=True)
    states = ListField(EmbeddedModelField('State'))
    cities = ListField(EmbeddedModelField('City'))
    counties = ListField(EmbeddedModelField('County'))

class State(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    percentage = models.FloatField()
    popularity = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

class City(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    percentage = models.FloatField()
    popularity = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

class County(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    percentage = models.FloatField()
    popularity = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()