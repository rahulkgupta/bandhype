#Quinn's code on reverse geo-coding for BandHype.
import json
import urllib

""" CHANGE THESE VARIABLES ACCORDINGLY """
input_file = 'city-location-test-data.txt'
output_file = 'city-location-test-data-output-1.txt'

f = open('city-location-test-data.txt', 'r')
o = open('city-location-test-data-output-tmp.txt', 'w')
MapQuest_API_KEY = """Fmjtd%7Cluuanua7n0%2C85%3Do5-96b054"""

""" 
Uses MapQuest API to reverse geocode. 
Takes in a latitude & longitude and outputs a dictionary with "city", "county", and "state" keys.
"""
def reverse_geocode(latitude, longitude):
    api_call = "http://www.mapquestapi.com/geocoding/v1/reverse?key=" + MapQuest_API_KEY + "&lat=" + str(latitude) + "&lng=" + str(longitude) + "&callback=renderReverse"
    fcc_api_call = "http://data.fcc.gov/api/block/find?format=json&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&showall=true"
    city = ""
    county = ""
    state = ""
    fips = ""
    try:
        response = urllib.urlopen(api_call).read()
        response_JSON = json.loads(response[response.find("{"):response.rfind("}")+1])

        """Uncomment the line below to view the JSON format"""
        # print json.dumps(response_JSON, sort_keys=True, indent=4)

        location = response_JSON["results"][0]["locations"][0]
        city = location["adminArea5"]
        # county = location["adminArea4"] # Replaced by FCC api call 
        state = location["adminArea3"]
    except:
        pass
    try:
        response = urllib.urlopen(fcc_api_call).read()
        response_JSON = json.loads(response)

        """Uncomment the line below to view the JSON format"""
        # print json.dumps(response_JSON, sort_keys=True, indent=4)

        county = response_JSON["County"]["name"]
        fips = response_JSON["County"]["FIPS"]
    except:
        pass
    return {"city": city, "county": county, "state": state, "fips": fips}

""" 
This main file reads an input_file, reverse geo-codes, 
and appends the city, county, state before writing it to the output_file. 
""" 
if __name__ == "__main__":
    try:
        f = open(input_file, 'r')
    except:
        print "Error opening input file: " + input_file + "."
        pass

    try:
        o = open(output_file, 'w')
    except:
        print "Error opening output file: " + output_file + "."
        pass

    try:
        for line in f:
            line = line.replace("\n", "") # Removes all "\n" tags
            data = line.split("\t")
            lonlat = eval(data[1])
            locations_dict = reverse_geocode(lonlat[1], lonlat[0])
            data.append(locations_dict["city"])
            # data.append(locations_dict["county"])
            data.append(locations_dict["state"])
            try:
                o.write("\t".join(data) + "\n")
            except:
                print "Error writing the data into output file in append_geo."
                pass

    except:
        print "Something went wrong in append_geo!"
        pass

    for line in f:
        data = line.split("\t")
        lonlat = eval(data[1])
        locations_dict = reverse_geocode(lonlat[1], lonlat[0])
        data.append(locations_dict["city"])
        data.append(locations_dict["county"])
        data.append(locations_dict["state"])
        data.append(locations_dict["fips"])
        try:
            o.write("\t".join(data) + "\n")
        except:
            pass

""" This code uses the city-db JSON to determine the cities of the tweets. """
# f = open('city-db.txt', 'r')
# r = open('city-location-test-data.txt', 'r')

# try:
#     city_db = json.loads(f.read())
# except:
#     print "city-db did not load correctly."

# def find_city(latitude, longitude):
#     for city, info in city_db.items():
#         if(((max(info["latitude_range"]) > latitude) and (latitude > min(info["latitude_range"]))) 
#             and ((max(info["longitude_range"]) > longitude) and (longitude > min(info["longitude_range"])))):
#             print city
#     #return "Corresponding city could not be found!"

# for line in r:
#     data = line.split("\t")
#     lonlat = eval(data[1])
#     find_city(lonlat[1], lonlat[0])   
     

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