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


# def icclistens(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 county_band = CountyBand.objects.get(band__name=arr[0], county__fips=arr[1])
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 county_band_count = CountyCount(
#                                 band=county_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[3]),
#                                 listen_pct=int(arr[4])
#                             )
#                 ## do some time stuff
#                 county_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

def ctalks(request):
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
                county_band = BandCounty(
                    band=band,
                    county=county,
                )
                county_band.times.append(time_obj)
                ## do some time stuff
                county_band.save()
            except:
                county_band = BandCounty(
                    band=band,
                    county=county,
                )
                county_band.times.append(time_obj)
                county_band.save()  
    return HttpResponse("success")

# def icccounts(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 county_band = CountyBand.objects.get(band__name=arr[0], county__fips=arr[1])
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 county_band_count = CountyCount(
#                                 band=county_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[3]),
#                                 listen_pct=int(arr[4]),
#                                 talk_count=int(arr[5]),
#                                 talk_pct=int(arr[6])
#                             )
#                 ## do some time stuff
#                 county_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

