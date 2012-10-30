import json

f = open('city-db.txt', 'r')
r = open('city-location-test-data.txt', 'r')

try:
    city_db = json.loads(f.read())
except:
    print "city-db did not load correctly."

def find_city(latitude, longitude):
    for city, info in city_db.items():
        if(((max(info["latitude_range"]) > latitude) and (latitude > min(info["latitude_range"]))) 
            and ((max(info["longitude_range"]) > longitude) and (longitude > min(info["longitude_range"])))):
            print city
    #return "Corresponding city could not be found!"

for line in r:
    data = line.split("\t")
    lonlat = eval(data[1])
    find_city(lonlat[1], lonlat[0])        

"""This code was used to filter for only US cities in CityCoordinatesList.txt"""
# f = open('CityCoordinatesList.txt')
# o = open('CityCoordinatesList-US.txt', 'w')

# for line in f:
#     if "United States of America" in line:
#         o.write(line)

"""This code was used to create city-db, a JSON file that has city names as keys and a latitude/longitude bounding box as the value"""
# f = open('CityCoordinatesList-US.txt', 'r')
# o = open('city-db.txt', 'w')
# city_db = dict()

# for line in f:
#     data = line.split("|")
#     latitude = []
#     longitude = []
#     for latlon in data[2].split(":"):
#         latlon = latlon.split(";")
#         latitude.append(latlon[0].strip())
#         longitude.append(latlon[1].strip())
    
#     northeast_bound = (max(latitude), max(longitude))
#     southwest_bound = (min(latitude), min(longitude))
#     latitude_range = (min(latitude), max(latitude))
#     longitude_range = (min(longitude), max(longitude))

#     city_db[data[1].strip()] = {"northeast_bound": northeast_bound, 
#     "southwest_bound": southwest_bound, "latitude_range": latitude_range, "longitude_range": longitude_range}
# o.write(json.dumps(city_db, sort_keys=True, indent=4))