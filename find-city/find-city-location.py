import json

# f = open('city-db.txt', 'r')

# try:
#     city_db = json.loads(f.read())
# except:
#     print "city-db did not load correctly."

# def find_city(latitude, longitude):
#     for key in city_db.keys():
#         if 
#     

city_db = dict()

"""This code was used to filter for only US cities in CityCoordinatesList.txt"""
# f = open('CityCoordinatesList.txt')
# o = open('CityCoordinatesList-US.txt', 'w')

# for line in f:
#     if "United States of America" in line:
#         o.write(line)

"""This code was used to create city-db, a JSON file that has city names as keys and a latitude/longitude bounding box as the value"""
# f = open('CityCoordinatesList-US.txt', 'r')
# o = open('city-db.txt', 'w')

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
#     city_db[data[1].strip()] = {"northeast_bound": northeast_bound, "southwest_bound": southwest_bound}
# o.write(json.dumps(city_db, sort_keys=True, indent=4))