import json
import urllib

MapQuest_API_KEY = """Fmjtd%7Cluuanua7n0%2C85%3Do5-96b054"""


#reverse geocode udf
@outputSchema("city:chararray, county: chararray, state: chararray")
def reverse_geocode(latitude, longitude):
    api_call = "http://www.mapquestapi.com/geocoding/v1/reverse?key=" + MapQuest_API_KEY + "&lat=" + str(latitude) + "&lng=" + str(longitude) + "&callback=renderReverse"
    city = ""
    county = ""
    state = ""
    try:
        response = urllib.urlopen(api_call).read()
        response_JSON = json.loads(response[response.find("{"):response.rfind("}")+1])

        """Uncomment the line below to view the JSON format"""
        # print json.dumps(response_JSON, sort_keys=True, indent=4)

        location = response_JSON["results"][0]["locations"][0]
        city = location["adminArea5"]
        county = location["adminArea4"]
        state = location["adminArea3"]
    except:
        pass
    return city, county, state

#fips udf
