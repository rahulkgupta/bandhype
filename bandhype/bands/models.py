from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=200)
    listen_count = models.IntegerField(null=True)
    listen_percentage = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class BandCount(models.Model):
    band = models.ForeignKey(Band)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_percentage = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class State(models.Model):
    name = models.CharField(max_length=200)
    abbr = models.CharField(max_length=4)
    fips = models.CharField(max_length=4, null=True)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    bands = models.ManyToManyField(Band, through='StateBand')

class StateBand(models.Model):
    band = models.ForeignKey(Band)
    state = models.ForeignKey(State)

class StateCount(models.Model):
    state_band = models.ForeignKey(StateBand)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_percentage = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class City(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    bands = models.ManyToManyField(Band, through='CityBand')

class CityBand(models.Model):
    band = models.ForeignKey(Band)
    city = models.ForeignKey(City)

class CityCount(models.Model):
    city_band = models.ForeignKey(CityBand)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_pct = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class County(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    fips = models.CharField(max_length=8)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    bands = models.ManyToManyField(Band, through='CountyBand')

class CountyBand(models.Model):
    band = models.ForeignKey(Band)
    county = models.ForeignKey(County)

class CountyCount(models.Model):
    county_band = models.ForeignKey(CountyBand)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_pct = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)