# Create your views here.
import json
import os
import time
from datetime import date

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import BandCounty, TimeCount


def ctalks(request):
    bands = {}
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/btc_f.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            band = arr[0]
            county = int(arr[1])
            time = arr[2]
            count = int(arr[3])
            pct = float(arr[4])
            time_obj = TimeCount(count=count,pct=pct,time=time)
            try:
                c_b = bands[band + "" + str(county)]
                c_b.times.append(time_obj)
                c_b.save()
            except:
                try:
                    county_band = BandCounty.objects.get(
                        band=band,
                        county=county,
                    )
                    county_band.times.append(time_obj)
                    ## do some time stuff
                    county_band.save()
                    bands[band + "" + str(county)] = county_band
                except:
                    county_band = BandCounty(
                        band=band,
                        county=county,
                    )
                    county_band.times.append(time_obj)
                    county_band.save()  
                    bands[band + "" + str(county)] = county_band
    return HttpResponse("success")
