import pymongo
import os
from pymongo import MongoClient


connection = MongoClient('ds033337.mongolab.com', 33337)
db = connection['heroku_app8819589']
db.authenticate('admin', 'twitter')
bands_band = db['bands_bandcity']
bands = {}
states = {"AL": "01","AK": "02", "AZ": "04","AR": "05","CA": "06",
    "CO":"08","CT":"09","DC": "10", "DE":"11","FL":"12","GA":"13","HI":"15","ID":"16",
    "IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24",
    "MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32",
    "NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37",
    "ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44",
    "SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50",
    "VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'btcy_f.txt')), 'r') as read_file:
        for line in read_file:
            arr = line.split(',')
            band_name = arr[0]
            city = arr[1].lower()
            state_fips = arr[2]
            time = arr[3]
            count = int(arr[4])
            pct = float(arr[5])
            state_abbr = ""
            for abbr, fips in states.iteritems():
                if state_fips == fips:
                    state_abbr = abbr
            time_obj = {"count":count,"pct":pct,"time":time}
            try:
                band = bands[band_name + city + state_fips]
                band["times"].append(time_obj)
                print "found"
            except:
                bands[band_name + city + state_fips] = {
                    "band": band_name,
                    "city": city,
                    "state_fips": state_fips,
                    "state_abbr": state_abbr,
                    "times" : [time_obj]
                }


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