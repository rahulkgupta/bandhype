# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import StateBand, State, Band

def isblistens(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/statebands.txt')), 'r') as read_file
        for line in read_file
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(
                    band__name=arr[0], 
                    state__fips=arr[1])
                
                state_band.listen_count = int(arr[2]) + state_band.listen_count
                state_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    state = State.objects.get(fips=arr[1])
                    state_band = StateBand(listen_count=int(arr[2]))
                    state_band.band = band
                    state_band.state = state 
                    state_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")

def isbtalks(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/statebands.txt')), 'r') as read_file
        for line in read_file
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(
                    band__name=arr[0], 
                    state__fips=arr[1])
                
                state_band.talk_count = int(arr[2]) + state_band.talk_count
                state_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    state = State.objects.get(fips=arr[1])
                    state_band = StateBand(talk_count=int(arr[2]))
                    state_band.band = band
                    state_band.state = state 
                    state_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")

def isb(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/statebands.txt')), 'r') as read_file
        for line in read_file
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(
                    band__name=arr[0], 
                    state__fips=arr[1]
                )
                state_band.listen_count = int(arr[2]) + state_band.listen_count
                state_band.talk_count = int(arr[3]) + state_band.talk_count
                state_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    state = State.objects.get(fips=arr[1])
                    state_band = StateBand(listen_count=int(arr[2]))
                    state_band = StateBand(talk_count=int(arr[3]))
                    state_band.band = band
                    state_band.state = state 
                    state_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")
