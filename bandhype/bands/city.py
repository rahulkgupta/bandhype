# # Create your views here.
# import json
# import os

# import operator

# from django.http import HttpResponse
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.conf import settings
# from django.core import serializers

# from bands.models import City, CityBand, State

# def listens(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/city.txt')), 'r') as read_file
#         for line in read_file
#             arr = line.split(',')
#             try:
#                 city_band = CityBand.objects.get(
#                     band__name = arr[0], 
#                     city__name = arr[1], 
#                     city__fips = arr[2]
#                     )
#                 city_band.listen_count = city_band.listen_count + int(arr[3])
#                 city_band.save()
#             except:
#                 city_band = CityBand()
#                 try:
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = City.objects.get(name=arr[1], fips=arr[2])
#                     city_band.listen_count = int(arr[3])
#                     city_band.save()
#                 except:
#                     city = City(name=arr[1], fips=arr[2])
#                     city.save()
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = city
#                     city_band.listen_count = int(arr[3])
#                     city_band.save()
#     return HttpResponse("success")

# def talks(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/city.txt')), 'r') as read_file
#         for line in read_file
#             arr = line.split(',')
#             try:
#                 city_band = CityBand.objects.get(
#                     band__name = arr[0], 
#                     city__name = arr[1], 
#                     city__fips = arr[2]
#                     )
#                 city_band.talk_count = city_band.talk_count + int(arr[3])
#                 city_band.save()
#             except:
#                 city_band = CityBand()
#                 try:
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = City.objects.get(name=arr[1], fips=arr[2])
#                     city_band.talk_count = int(arr[3])
#                     city_band.save()
#                 except:
#                     city = City(name=arr[1], fips=arr[2])
#                     city.save()
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = city
#                     city_band.talk_count = int(arr[3])
#                     city_band.save()
#     return HttpResponse("success")

# def counts(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/city.txt')), 'r') as read_file
#         for line in read_file
#             arr = line.split(',')
#             try:
#                 city_band = CityBand.objects.get(
#                     band__name = arr[0], 
#                     city__name = arr[1], 
#                     city__fips = arr[2]
#                     )
#                 city_band.listen_count = city_band.listen_count + int(arr[3])
#                 city_band.talk_count = city_band.talk_count + int(arr[4])
#                 city_band.save()
#             except:
#                 city_band = CityBand()
#                 try:
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = City.objects.get(name=arr[1], fips=arr[2])
#                     city_band.listen_count = int(arr[3])
#                     city_band.talk_count = int(arr[4])
#                     city_band.save()
#                 except:
#                     city = City(name=arr[1], fips=arr[2])
#                     city.save()
#                     city_band.band = Band.objects.get(name=arr[0])
#                     city_band.city = city
#                     city_band.listen_count = int(arr[3])
#                     city_band.talk_count = int(arr[4])
#                     city_band.save()
#     return HttpResponse("success")
