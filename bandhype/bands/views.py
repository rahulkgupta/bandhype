# Create your views here.
import json
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers


from bands.models import Band, State, County, Fips
def home(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))

def promoters(request):
    return render_to_response('promoters.html', {},context_instance=RequestContext(request))

def bands(request):
    return render_to_response('bands.html', {},context_instance=RequestContext(request))

def counties(request):
    json_data = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/json/us-counties.json'))).read()
    data1 = json.dumps(json_data)
    return HttpResponse(json_data, mimetype="application/json")

def states(request):
    json_data = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/json/us-states.json'))).read()
    data1 = json.dumps(json_data)
    return HttpResponse(json_data, mimetype="application/json")

def unemployment(request):
    json_data = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/json/unemployment.json'))).read()
    data1 = json.dumps(json_data)
    return HttpResponse(json_data , mimetype="application/json")

def countrypop(request):
    band_name = request.GET['query']
    try: 
        band = Band.objects.get(name=band_name)
        counties = {}
        for county in band.counties:
            counties[county.fips] = county.count
        return HttpResponse(json.dumps(counties), mimetype="application/json")
    except:
        return HttpResponse("nothing")

# def fips(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/fips_use.txt')), 'r') as fips:
#         for line in fips:
#             print line
#             fips_line = line.split(',')
#             # print fips_line[0] + " "  +fips_line[3]
#             fips = Fips(county=fips_line[1].lower(),
#                         state=fips_line[0], 
#                         county_fips=fips_line[3].rstrip(), state_fips=fips_line[2])
#             fips.save()

#     return render_to_response('index.html', {},context_instance=RequestContext(request))

def bcc(request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/banded_county_count.txt')), 'r') as bcc:
        for line in bcc:
            bcc_line = line.split(',')

            county = bcc_line[2]
            state = bcc_line[1]
            count = int(bcc_line[3])

            saint = county[0:3]
            city_par = county[-6:]
            miami = county[0:5]

            if city_par == "(City)":
                county = county[:-7] + " city"

            if county == "Dekalb" and not state == "MO" and not state == "TN":
                county = "De Kalb"

            if not state == "ON" and not state == "BC" and not state == "BC" and not state == "QC":
                county = county.lower()
                try:
                    fips = Fips.objects.get(county=county.replace("'", ""), state=bcc_line[1])
                    band_name = bcc_line[0]
                    # print fips.state_fips + fips.county_fips
                    county_obj = County(name=county, fips=fips.state_fips + fips.county_fips,count=count)
                    try:
                        band = Band.objects.get(name=band_name)
                        band.counties.append(county_obj)
                        band.save()
                    except:
                        band = Band(name=band_name)
                        band.counties.append(county_obj)
                        band.save()
                except:
                    print county + " " + state
                        
    return render_to_response('index.html', {},context_instance=RequestContext(request)) 





