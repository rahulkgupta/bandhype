from django.db import models
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField

class Band(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    popularity = models.FloatField(null=True)
    time = models.DateField(null=True)
    states = ListField(EmbeddedModelField('State'))
    cities = ListField(EmbeddedModelField('City'))
    counties = ListField(EmbeddedModelField('County'))

class State(models.Model):
    name = models.CharField(max_length=200)
    fips = models.CharField(max_length=8)
    count = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    popularity = models.FloatField(null=True)

class City(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    popularity = models.FloatField(null=True)

class County(models.Model):
    name = models.CharField(max_length=200)
    fips = models.CharField(max_length=8)
    count = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    popularity = models.FloatField(null=True)

class Fips(models.Model):
    county = models.CharField(max_length=200)
    state = models.CharField(max_length=4)
    county_fips = models.CharField(max_length=4)
    state_fips = models.CharField(max_length=4)
