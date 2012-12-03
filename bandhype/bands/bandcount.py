# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import Band, TimeCount


# def insertbandcountslistens(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 band = Band.objects.get(name=arr[0])
#                 band_count = BandCount(
#                                 band=band, 
#                                 time=arr[1], 
#                                 listen_count=int(arr[2]),
#                                 listen_pct=int(arr[3])
#                             )
#                 ## do some time stuff
#                 band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")
def btalks(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bt_f.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            band = arr[0]
            time = arr[1]
            count = int(arr[2])
            pct = float(arr[3])
            time_obj = TimeCount(count=count,pct=pct,time=time)
            try:
                band = Band.objects.get(
                    band=band,
                )
                band.times.append(time_obj)
                ## do some time stuff
                band.save()
            except:
                band = Band(
                    band=band,
                )
                band.times.append(time_obj)
                band.save()  
    return HttpResponse("success")

# def insertbandcountstalks(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandstalks.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 band = Band.objects.get(name=arr[0])
#                 band_count = BandCount(
#                                 band=band, 
#                                 time=arr[1], 
#                                 talk_count=int(arr[2]),
#                                 talk_pct=int(arr[3])
#                             )
#                 band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

# def insertbandcounts(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bands.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 band = Band.objects.get(name=arr[0])
#                 band_count = BandCount(
#                                 band=band, 
#                                 time=arr[1],
#                                 listen_count=int(arr[2]),
#                                 listen_pct=int(arr[3])
#                                 talk_count=int(arr[4]),
#                                 talk_pct=int(arr[5])
#                             )
#                 band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

