# Create your views here.
import json
import os
import time

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

# from bands.models import State, County, Band

from bands.models import Band, BandCity, BandState, BandCounty, TimeCount

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
    print band_name 
    query = BandCounty.objects.filter(band=band_name)
    counties = {}
    for bc in query:
        county = str(bc.county)
        if len(county) == 4:
            print county
            county = str(0) + county
        bc_county = counties[county] = []
        for time_count in bc.times:
            counties[county].append((time_count.time, time_count.pct, time_count.count))
        bc_county.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(counties, indent=2), mimetype="application/json")


def timeband(request):
    band_name = request.GET['query']
    print band_name 
    query = Band.objects.get(band=band_name)
    times = []
    for time in query.times:
        times.append((time.time, time.count, time.pct))
        times.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(times, indent=2), mimetype="application/json")
# #commented out so that the requests don't get accidentally fired
# def fips(request):
#     for county in County.objects.all():
#         if len(county.fips) == 3:
#             county.fips = county.state.fips + county.fips
#             county.save()
#     return render_to_response('index.html', {},context_instance=RequestContext(request))

# def bcc(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/banded_county_count.txt')), 'r') as bcc:
#         for line in bcc:
#             bcc_line = line.split(',')

#             county = bcc_line[2]
#             state = bcc_line[1]
#             count = int(bcc_line[3])

#             saint = county[0:3]
#             city_par = county[-6:]
#             miami = county[0:5]

#             if city_par == "(City)":
#                 county = county[:-7] + " city"

#             if county == "Dekalb" and not state == "MO" and not state == "TN":
#                 county = "De Kalb"

#             if not state == "ON" and not state == "BC" and not state == "BC" and not state == "QC":
#                 county = county.lower()
#                 try:
#                     fips = Fips.objects.get(county=county.replace("'", ""), state=bcc_line[1])
#                     band_name = bcc_line[0]
#                     # print fips.state_fips + fips.county_fips
#                     county_obj = County(name=county, fips=fips.state_fips + fips.county_fips,count=count)
#                     try:
#                         band = Band.objects.get(name=band_name)
#                         band.counties.append(county_obj)
#                         band.save()
#                     except:
#                         band = Band(name=band_name)
#                         band.counties.append(county_obj)
#                         band.save()
#                 except:
#                     print county + " " + state
                        
#     return render_to_response('index.html', {},context_instance=RequestContext(request)) 

# def bsc(request):
#     states = ["AL","AK", "AZ","AR","CA",
#"CO","CT","DE","FL","GA","HI","ID",
#             "IL","IN","IA","KS","KY","LA","ME","MD",
#             "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC",
#             "ND","OH","OK","OR","PA","RI",
#"SC","SD","TN","TX","UT","VT",
#             "VA","WA","WV","WI","WY"]
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/banded_state_count.txt')), 'r') as bsc:
#         for line in bsc:
#             bsc_line = line.split(',')
#             band_name = bsc_line[0]
#             state = bsc_line[1]
#             count = int(bsc_line[2])
#             state_obj = State(name=state, count=count)
#             if state in states:
#                 try:
#                     band = Band.objects.get(name=band_name)
#                     band.states.append(state_obj)
#                     band.save()
#                 except:
#                     print "failed"
#     return render_to_response('index.html', {},context_instance=RequestContext(request))         



# def getfips(request):
#     county = request.GET['county'].lower().replace(" ", "")
#     state = request.GET['state']
#     try:
#         fips = Fips.objects.get(county=county, state=state)
#         response = {"response": "success", "fips": fips.county_fips}
#         return HttpResponse(json.dumps(response), mimetype="application/json")
#     except:
#         response = {"response": "failure"}
#         return HttpResponse(json.dumps(response), mimetype="application/json")


# def topstate(request):
#     state_name = request.GET['state'].upper()
#     bands = Band.objects.raw_query({"states.name" : state_name})
#     response = {}
#     for band in bands:
#         for state in band.states:
#             if state.name == state_name:
#                 response[band.name] = state.count
#     sorted_response = sorted(response.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]
#     return HttpResponse(json.dumps(sorted_response), mimetype="application/json")


# def state(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/fipsstates.txt')), 'r') as fips:
#         for line in fips:
#             print line
#             fips_line = line.split(',')
#             # print fips_line[0] + " "  +fips_line[3]
#             state = State(name=fips_line[1],fips=fips_line[0],abbr=fips_line[2])
#             state.save()

#     return render_to_response('index.html', {},context_instance=RequestContext(request))




