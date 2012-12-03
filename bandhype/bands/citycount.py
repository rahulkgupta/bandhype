# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import BandCity, TimeCount

def citytalks(request):
    bands = {}
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/btcy_f.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            band = arr[0]
            city = arr[1].lower()
            state = int(arr[2])
            time = arr[3]
            count = int(arr[4])
            pct = float(arr[5])
            time_obj = TimeCount(count=count,pct=pct,time=time)
            try:
                city_band = BandCity.objects.get(
                    band=band,
                    city=city,
                    state_fips=state,
                )
                city_band.times.append(time_obj)
                ## do some time stuff
                city_band.save()
            except:
                city_band = BandCity(
                    band=band,
                    city=city,
                    state_fips=state,
                )
                city_band.times.append(time_obj)
                city_band.save()  
    return HttpResponse("success")
