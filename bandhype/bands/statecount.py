# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import StateBand, StateCount


def isclistens(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(band__name=arr[0], state__fips=arr[1])
                state_band_count = StateCount(
                                band=state_band, 
                                time=arr[2], 
                                listen_count=int(arr[3]),
                                listen_pct=int(arr[4])
                            )
                ## do some time stuff
                state_band_count.save()
            except:
                return HttpResponse('error')
    return HttpResponse("success")

def isctalks(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(band__name=arr[0], state__fips=arr[1])
                state_band_count = StateCount(
                                band=state_band, 
                                time=arr[2], 
                                talk_count=int(arr[3]),
                                talk_pct=int(arr[4])
                            )
                ## do some time stuff
                state_band_count.save()
            except:
                return HttpResponse('error')
    return HttpResponse("success")

def isccounts(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                state_band = StateBand.objects.get(band__name=arr[0], state__fips=arr[1])
                state_band_count = StateCount(
                                band=state_band, 
                                time=arr[2], 
                                listen_count=int(arr[3]),
                                listen_pct=int(arr[4]),
                                talk_count=int(arr[5]),
                                talk_pct=int(arr[6])
                            )
                ## do some time stuff
                state_band_count.save()
            except:
                return HttpResponse('error')
    return HttpResponse("success")

