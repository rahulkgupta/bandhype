# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))

def promoters(request):
    return render_to_response('promoters.html', {},context_instance=RequestContext(request))

def bands(request):
    return render_to_response('bands.html', {},context_instance=RequestContext(request))