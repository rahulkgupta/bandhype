from django.db import models
from djangotoolbox.fields import ListField

class Band(models.Model):
    name = models.CharField()
    tweets = models.IntegerField()
    popularity = models.DecimalField(max_digits=19, decimal_places=10)