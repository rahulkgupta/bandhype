# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import Band

def insertbandslistens(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as bands:
        for line in bands:
            arr = line.split(',')
            try:
                band = Band.objects.get(name=arr[0])
                band.listen_count = int(arr[1]) + band.listen_count
                band.save()
            except:
                band = Band(name=arr[0])
                band.listen_count = int(arr[1])
                band.save()
    return HttpResponse("success")

def insertbandstalks(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandstalks.txt')), 'r') as bands:
        for line in bands:
            arr = line.split(',')
            try:
                band = Band.objects.get(name=arr[0])
                band.talk_count = int(arr[1]) + band.talk_count
                band.save()
            except:
                band = Band(name=arr[0])
                band.talk_count = int(arr[1])
                band.save()
    return HttpResponse("success")

def insertbands(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bands.txt')), 'r') as bands:
        for line in bands:
            arr = line.split(',')
            try:
                band = Band.objects.get(name=arr[0])
                band.listen_count = int(arr[1]) + band.listen_count
                band.talk_count = int(arr[2]) + band.talk_count
                band.save()
            except:
                band = Band(name=arr[0])
                band.listen_count = int(arr[1])
                band.talk_count = int(arr[2])
                band.save()
    return HttpResponse("success")
