from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=200)
    listen_count = models.IntegerField(null=True)
    listen_percentage = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class Counts(models.Model):
    band = models.ForeignKey(Band)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_percentage = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class State(models.Model):
    name = models.CharField(max_length=4)
    fips = models.CharField(max_length=4, null=True)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)
    talks = models.ManyToManyField(Band, through='StateTalks')

class StateTalks(models.Model):
    band = models.ForeignKey(Band)
    state = models.ForeignKey(State)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_pct = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)

class City(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    count = models.IntegerField(null=True)
    pct = models.FloatField(null=True)

class CityTalks(models.Model):
    band = models.ForeignKey(Band)
    city = models.ForeignKey(City)
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

class CountyTalks(models.Model):
    band = models.ForeignKey(Band)
    county = models.ForeignKey(County)
    time = models.DateField(null=True)
    listen_count = models.IntegerField(null=True)
    listen_pct = models.FloatField(null=True)
    talk_count = models.IntegerField(null=True)
    talk_pct = models.FloatField(null=True)