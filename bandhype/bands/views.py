# Create your views here.
import json
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

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