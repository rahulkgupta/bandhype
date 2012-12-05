from django.db import models
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

class Band(models.Model):
    band = models.CharField(max_length=200)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    times = ListField(EmbeddedModelField('TimeCount'))

class BandState(models.Model):
    band = models.CharField(max_length=200)
    state_fips = models.IntegerField()
    state_abbr = models.CharField(max_length=200, null=True)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    times = ListField(EmbeddedModelField('TimeCount'))
    
class BandCity(models.Model):
    band = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state_fips = models.CharField(max_length=200)
    state_abbr = models.CharField(max_length=200, null=True)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    times = ListField(EmbeddedModelField('TimeCount'))

class BandCounty(models.Model):
    band = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    times = ListField(EmbeddedModelField('TimeCount'))

class TimeCount(models.Model):
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    time = models.CharField(max_length=12)
