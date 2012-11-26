# Create your views here.
import json
import os

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

from bands.models import CountyBand, County, Band

def icblistens(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/countybands.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                county_band = CountyBand.objects.get(
                    band__name=arr[0], 
                    county__fips=arr[1])
                
                county_band.listen_count = int(arr[2]) + county_band.listen_count
                county_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    county = County.objects.get(fips=arr[1])
                    county_band = CountyBand(listen_count=int(arr[2]))
                    county_band.band = band
                    county_band.county = county 
                    county_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")

def icbtalks(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/countybands.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                county_band = CountyBand.objects.get(
                    band__name=arr[0], 
                    county__fips=arr[1])
                
                county_band.talk_count = int(arr[2]) + county_band.talk_count
                county_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    county = County.objects.get(fips=arr[1])
                    county_band = CountyBand(talk_count=int(arr[2]))
                    county_band.band = band
                    county_band.county = county 
                    county_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")

def icb(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/CountyBands.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            try:
                county_band = CountyBand.objects.get(
                    band__name=arr[0], 
                    county__fips=arr[1]
                )
                county_band.listen_count = int(arr[2]) + county_band.listen_count
                county_band.talk_count = int(arr[3]) + county_band.talk_count
                county_band.save()
            except:
                try:
                    band = Band.objects.get(name=arr[0])
                    county = County.objects.get(fips=arr[1])
                    county_band = CountyBand(listen_count=int(arr[2]))
                    county_band = CountyBand(talk_count=int(arr[3]))
                    county_band.band = band
                    county_band.county = county 
                    county_band.save()
                except:
                    return HttpResponse('error')
    return HttpResponse("success")
