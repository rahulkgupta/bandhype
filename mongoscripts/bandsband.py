import pymongo
import os
from pymongo import MongoClient
import re

connection = MongoClient('ds033337.mongolab.com', 33337)
db = connection['heroku_app8819589']
db.authenticate('admin', 'twitter')
bands_band = db['bands_listen']
bands = {}
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'bt_f.txt')), 'r') as read_file:
        for line in read_file:
            try:
                arr = line.split(';')
                band_name = ""
                time = ""
                count = 0
                pct = 0
                pos = 0
                band_name = arr[0]
                time = arr[1]
                count = int(arr[2])
                pct = float(arr[3])

                print count, pct
                time_obj = {"count":count,"pct":pct,"time":time}
                try:
                    band = bands[band_name]
                    band["times"].append(time_obj)
                    print "found"
                except:
                    bands[band_name] = {"band": band_name, "times" : [time_obj]}
            except:
                print "nahhhh"

for band_name in bands:
    band = bands[band_name]
    band['pct'] = 0
    band['count'] = 0
    for time in band['times']:
        band['count']+= time["count"]
        band['pct'] += time["pct"]
    band['pct'] = band['pct']/len(band['times'])

bands_band.insert(bands.values())