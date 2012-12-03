# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import BandState, TimeCount


# def isclistens(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 state_band = StateBand.objects.get(band__name=arr[0], state__fips=arr[1])
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 state_band_count = StateCount(
#                                 band=state_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[3]),
#                                 listen_pct=int(arr[4])
#                             )
#                 ## do some time stuff
#                 state_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

def stalks(request):
    bands = {}
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bts_f.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            band = arr[0]
            state_fips = int(arr[1])
            time = arr[2]
            count = int(arr[3])
            pct = float(arr[4])
            time_obj = TimeCount(count=count,pct=pct,time=time)

            try:
                s_b = bands[band + "" + str(state_fips)]
                s_b.times.append(time_obj)
                s_b.save()
            except:
                try:
                    state_band = BandState.objects.get(
                        band=band,
                        state_fips=state_fips,
                    )
                    state_band.times.append(time_obj)
                    ## do some time stuff
                    state_band.save()
                    bands[band + "" + str(state_fips)] = state_band
                except:
                    state_band = BandState(
                        band=band,
                        state_fips=state_fips,
                    )
                    state_band.times.append(time_obj)
                    state_band.save()
                    bands[band + " " + str(state_fips)] = state_band
    return HttpResponse("success")

# def isccounts(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/bandslistens.txt')), 'r') as read_file:
#         for line in read_file:
#             arr = line.split(',')
#             try:
#                 state_band = StateBand.objects.get(band__name=arr[0], state__fips=arr[1])
#                 count_time = date.fromtimestamp(time.strptime(arr[2],'%a %b %d %H:%M:%S +0000 %Y'))
#                 state_band_count = StateCount(
#                                 band=state_band, 
#                                 time=count_time, 
#                                 listen_count=int(arr[3]),
#                                 listen_pct=int(arr[4]),
#                                 talk_count=int(arr[5]),
#                                 talk_pct=int(arr[6])
#                             )
#                 ## do some time stuff
#                 state_band_count.save()
#             except:
#                 return HttpResponse('error')
#     return HttpResponse("success")

