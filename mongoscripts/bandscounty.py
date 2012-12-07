import pymongo
import os
from pymongo import MongoClient


connection = MongoClient('ds033337.mongolab.com', 33337)
db = connection['heroku_app8819589']
db.authenticate('admin', 'twitter')
bands_band = db['bands_listencounty']
bands = {}
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'btc_f.txt')), 'r') as read_file:
        for line in read_file:
            try:
                arr = line.split(';')
                band_name = arr[0]
                county = arr[1]
                time = arr[2]
                count = int(arr[3])
                pct = float(arr[4])
                time_obj = {"count":count,"pct":pct,"time":time}
                try:
                    band = bands[band_name + "" + str(county)]
                    band["times"].append(time_obj)
                    print "found"
                except:
                    bands[band_name + "" + str(county)] = {
                        "band": band_name,
                        "county": county,
                        "times" : [time_obj]
                    }
            except:
                print "not happening"

for band_name in bands:
    band = bands[band_name]
    band['pct'] = 0
    band['count'] = 0
    for time in band['times']:
        band['count']+= time["count"]
        band['pct'] += time["pct"]
    band['pct'] = band['pct']/len(band['times'])
    print band

bands_band.insert(bands.values())