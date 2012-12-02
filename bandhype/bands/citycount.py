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


# def citylistens(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 city_band = CityBand.objects.get(
#                     band__name=arr[0], 
#                     city__name=arr[1],
#                     city__state__fips=arr[2]
#                 )
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 city_band_count = CityCount(
#                                 band=city_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[4]),
#                                 listen_pct=int(arr[5])
#                             )
#                 ## do some time stuff
#                 city_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

# def citytalks(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/btcy_f.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             band = arr[0]
#             city = arr[1].lower()
#             state = int(arr[2])
#             time = arr[3]
#             count = int(arr[4])
#             pct = float(arr[5])
#             time_obj = TimeCount(count=count,pct=pct,time=time)
#             try:
#                 city_band = BandCity(
#                     band=band,
#                     city=city,
#                     state_fips=state,
#                 )
#                 city_band.times.append(time_obj)
#                 ## do some time stuff
#                 city_band.save()
#             except:
#                 city_band = BandCity(
#                     band=band,
#                     city=city,
#                     state_fips=state,
#                 )
#                 city_band.times.append(time_obj)
#                 city_band.save()  
#     return HttpResponse("success")

# def citycounts(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 city_band = CityBand.objects.get(
#                     band__name=arr[0], 
#                     city__name=arr[1],
#                     city__state__fips=arr[2]
#                 )
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 city_band_count = CityCount(
#                                 band=city_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[4]),
#                                 listen_pct=int(arr[5]),
#                                 talk_count=int(arr[6]),
#                                 talk_pct=int(arr[7])
#                             )
#                 ## do some time stuff
#                 city_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

