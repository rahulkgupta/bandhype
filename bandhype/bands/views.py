# Create your views here.
import json
import os
import time

import operator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core import serializers

# from bands.models import State, County, Band

from bands.models import Band, Listen, BandCity, BandState, BandCounty, ListenCounty, TimeCount, ListenCity

def home(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))

def promoters(request):
    return render_to_response('promoters.html', {},context_instance=RequestContext(request))

def bands(request):
    band_json = ["chvrches", "katy perry", "the raconteurs", "maroon 5", "hoobastank", 
    "zz top", "taylor swift", "judas priest", "goldfinger", "lindsey stirling", "sonic youth", 
    "gogol bordello", "kraddy", "phantom planet", "hatebreed", "wolfmother", "powerman 5000", 
    "george winston", "white stripes", "jason mraz", "junior senior", "james blunt", 
    "bob marley", "tangerine dream", "flyleaf", "sister sledge", "skism", "gordon lightfoot", 
    "nicki minaj", "the fray", "chris brown", "white zombie", "sum 41", "mr c", "keyshia cole", 
    "flaming lips", "blink 182", "sugarcult", "the fratellis", "new boyz", "kenny chesney", 
    "the lumineers", "deadmau5", "haddaway", "avicii", "rascal flatts", "jon pardi", 
    "lil wayne", "willie nelson", "eminem", "beck", "greg bates", "cherub", "leighton meester", 
    "buffalo springfield", "nadia ali", "miracle drug", "glee cast", "rusko", "indigo girls", 
    "eve 6", "gorillaz", "jefferson airplane", "krewella", "justin timberlake", "pantera", 
    "iron maiden", "christina perri", "casey james", "the remote", "zedd", "rob dougan", 
    "odetta", "citizen king", "pit bull", "coldplay", "prince royce", "bon jovi", "trace adkins","afrojack", "ratatat", "van halen", "sufjan stevens", "beastie boys", "m83", "muse", "berlin","train", "bloodhound gang", "gary allan", "miranda lambert", "calvin harris", "gwen stefani","godsmack", "grimes", "rolling stones", "generation x", "alex clare", "knife party", "stroke","morning parade", "chevelle", "bonnie tyler", "public enemy", "santana", "hollywood undead","tim mcgraw", "blaqk audio", "hugo", "snow patrol", "sneaker pimps", "drowning pool","duran duran", "lostprophets", "lacuna coil", "ed sheehan", "eric church", "freestylers","the killers", "daddy yankee", "django django", "cascada", "darius rucker", "pistol annies","tal bachman", "staind", "willow", "jeffree star", "beyonce", "major lazer", "stone sour","nelly furtado", "shania twain", "elliott smith", "smash mouth", "buckcherry", "mgmt", 
    "blackmill", "eric clapton", "lynyrd skynyrd", "deftones", "clutch", "dido", "chris cagle", 
    "matchbox twenty", "blind melon", "thompson square", "the cardigans", "marilyn manson", 
    "ozzy osborne", "randy houser", "amo ellas", "barenaked ladies", "don omar", "neon trees", 
    "jay z", "dire straits", "evanescence", "vertical horizon", "garvey", "jessie j", 
    "aqualung", "spice girls", "jeff buckley", "rem", "paul mccartney", "leo kottke", 
    "white town", "led zeppelin", "king crimson", "oasis", "bear mccreary", "ben folds", 
    "kristen kelly", "ok go", "metallica", "collective soul", "tomahawk", "estelle", 
    "bad brains", "disturbed", "the hives", "smashing pumpkins", "david archuleta", 
    "bon iver", "the smiths", "the beatles", "linkin park", "bjork", "grateful dead", 
    "james brown", "madeon", "imagine dragons", "miles davis", "genesis", "adventure club", 
    "kt tunstall", "postal service", "ellie goulding", "tool", "nirvana", "the cataracs", 
    "lcd soundsystem", "king missile", "clannad", "the skatalites", "frou fro", 
    "howlin wolf", "martin solveig", "pretty lights", "steve earle", "one direction", 
    "orgy", "muddy waters", "adam lambert", "trey anastasio", "candlebox", "velvet revolver", 
    "dan black", "peter gabriel", "brantley gilbert", "kacey musgraves", "adele", 
    "little dragon", "modest mouse", "luke bryan", "franz ferdinand", "sick puppies", 
    "foreigner", "the buggles", "the bled", "missy elliott", "the weeknd", "la roux", 
    "stabbing westward", "limp bizket", "everlast", "daughtry", "ac dc", "rancid", 
    "slipknot", "kip moore", "janis joplin", "good charlotte", "david guetta", 
    "reba mcentire", "queen", "eurythmics", "mutemath", "danny elfman", "volbeat", 
    "tenacious d", "enrique iglesias", "gotye", "alexander acha", "borgore", "rihanna", 
    "bush", "chopin", "fuel", "don mclean", "the byrds", "violent femmes", "leann rimes", 
    "oakenfold", "juicy j", "james taylor", "avenged sevenfold", "justin moore", 
    "citizen cope", "george strait", "porter robinson", "romeo santos", "the clash", 
    "dillon", "carlos vives", "bruce springsteen", "phil collins", "alanis morissette", 
    "sheryl crow", "soundgarden", "emmylou harris", "celtic woman", "bridget mendler", 
    "apollo 440", "the script", "toby keith", "motley crue", "neil young", "halestorm", 
    "brassica", "porcelain black", "apocolyptica", "foo fighters", "pearl jam", 
    "marcy playground", "lady sovereign", "black sabbath", "priestess", "kelly rowland", 
    "sublime", "no doubt", "harry chaplin", "lady antebellum", "placebo", "melanie fiona", 
    "the prodigy", "audioslave", "christina aguilera", "alicia keys", "alice cooper", 
    "the pretenders", "oingo boingo", "michael jackson", "gin blossoms", "imogen heap", 
    "jimi hendrix", "atrey", "china man", "lee brice", "asher roth", "the darkness", 
    "devotchka", "sevendust", "alexandra stan", "billy joel", "timbaland", "moody blues", 
    "frank zappa", "savage garden", "nickelback", "massive attack", "benny benassi", 
    "the bravery", "onerepublic", "the wanted", "jack white", "die antwood", "styx", 
    "soil", "sting", "kelly clarkson", "butthole surfers", "the who", "madonna", 
    "flogging molly", "rob thomas", "tony bennett", "jawbreaker", "tim mcmorris", 
    "semisonic", "rob zombie", "ween", "blake shelton", "everclear", "carrie underwood", 
    "cassadee pope", "lou bega", "stateless", "jake owens", "moby", "pitbull", 
    "alejandro sanz", "bassnecter", "lightning bolt", "peeping tom", "ciara", 
    "blue foundation", "parov stelar", "bob dylan", "50 cent", "portishead", 
    "sugar ray", "breaking benjamin", "darude", "eric prydz", "steely dan", 
    "adema", "def leppard", "beach boys", "newcleus", "lovage", "jethro tull", 
    "laura gibson", "the cure", "crystal castles", "depeche mode", "creed", 
    "lena", "crazy town", "usher", "incubus", "zero 7", "radiohead", "shakira", 
    "lifehouse", "bruno mars", "amanda brown", "the used", "chainz", "dustin lynch", 
    "joy division", "hinder", "lmfao", "papa roach", "skrillex", "akon", "aerosmith", 
    "eiffel 65", "silversun pickups", "owl city", "flux pavilion", "fleetwood mac", 
    "ben howard", "the dreaming", "disclosure", "garbage", "trust company", 
    "britney spears", "eighteen visions", "thomas newman", "tracy chapman", 
    "cobra starship", "pink floyd", "jason derulo", "tantric", "don davis", 
    "green day", "jason aldean", "kylie minogue", "nashville cast", "madilyn bailey", 
    "cher lloyd", "melanie martinez", "gnarls barkley", "symphony x", "awolnation", 
    "seether", "pinkly smooth", "easton corbin", "rudimental", "hunter hayes", "fiona apple", 
    "counting crows", "purity ring", "chromeo", "sbtrkt", "the vines", "sex pistols", 
    "ghost town", "cake", "jose feliciano", "daft punk", "kid rock", "lady gaga", "monsta", 
    "nero", "teenage days", "bingo players", "shinedown", "french montana", "justin bieber", 
    "korn", "david bowie", "george gershwin", "otto knows", "enya", "jennifer lopez", 
    "mike posner", "bag raiders", "icona pop", "the offspring", "rita ora", "thomas rhett", 
    "the misfits"]
    return render_to_response('bands.html', {"bands": json.dumps(band_json)},context_instance=RequestContext(request))

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

def countrypop(request):
    band_name = request.GET['query']
    print band_name 
    bandcounties = BandCounty.objects.filter(band=band_name)
    band = Band.objects.get(band=band_name)
    counties = {}
    for bc in bandcounties:
        county = str(bc.county)
        if len(county) == 4:
            print county
            county = str(0) + county
        bc_county = counties[county] = []
        for time_count in bc.times:
            counties[county].append((time_count.time, time_count.pct, time_count.count))
        bc_county.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(counties, indent=2), mimetype="application/json")


def timeband(request):
    band_name = request.GET['query'].lower()
    query = Band.objects.get(band=band_name)
    times = []
    for time in query.times:
        times.append((time.time, time.count, time.pct))
        times.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(times, indent=2), mimetype="application/json")

def countrylisten(request):
    band_name = request.GET['query']
    print band_name 
    bandcounties = ListenCounty.objects.filter(band=band_name)
    band = Band.objects.get(band=band_name)
    counties = {}
    for bc in bandcounties:
        county = str(bc.county)
        if len(county) == 4:
            print county
            county = str(0) + county
        bc_county = counties[county] = []
        for time_count in bc.times:
            counties[county].append((time_count.time, time_count.pct, time_count.count))
        bc_county.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(counties, indent=2), mimetype="application/json")


def timelisten(request):
    band_name = request.GET['query'].lower()
    query = Listen.objects.get(band=band_name)
    times = []
    for time in query.times:
        times.append((time.time, time.count, time.pct))
        times.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(times, indent=2), mimetype)

def getcity(request):
    city_name = request.GET['city'].lower()
    states = {"AL": "01","AK": "02", "AZ": "04","AR": "05","CA": "06",
            "CO":"08","CT":"09","DC": "10", "DE":"11","FL":"12","GA":"13","HI":"15","ID":"16",
            "IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24",
            "MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32",
            "NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37",
            "ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44",
            "SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50",
            "VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
    state_fips = states[request.GET['state'].upper()]
    query = BandCity.objects.filter(
            city = city_name,
            state_fips = state_fips
        ).order_by('-count')[:10]
    bands = []
    for bc in query:
        band = {}
        bands.append(band)
        band["band"] = bc.band
        band["pct"] = bc.pct
        band["count"] = bc.count
        times = band["times"] = []
        for time_count in bc.times:
            times.append((time_count.time, time_count.pct, time_count.count))
        times.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(bands, indent=2), mimetype="application/json")

def listencity(request):
    city_name = request.GET['city'].lower()
    states = {"AL": "01","AK": "02", "AZ": "04","AR": "05","CA": "06",
            "CO":"08","CT":"09","DC": "10", "DE":"11","FL":"12","GA":"13","HI":"15","ID":"16",
            "IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24",
            "MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32",
            "NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37",
            "ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44",
            "SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50",
            "VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
    state_fips = states[request.GET['state'].upper()]
    query = ListenCity.objects.filter(
            city = city_name,
            state_fips = state_fips
        ).order_by('-count')[:10]
    bands = []
    for bc in query:
        band = {}
        bands.append(band)
        band["band"] = bc.band
        band["pct"] = bc.pct
        band["count"] = bc.count
        times = band["times"] = []
        for time_count in bc.times:
            times.append((time_count.time, time_count.pct, time_count.count))
        times.sort(key=lambda time_count: time_count[0])
    return HttpResponse(json.dumps(bands, indent=2), mimetype="application/json")


def promoterlistens(request):
    return render_to_response('promoterlistens.html', {},context_instance=RequestContext(request))


def bandlistens(request):
    band_json = ["chvrches", "katy perry", "the raconteurs", "maroon 5", "hoobastank", 
    "zz top", "taylor swift", "judas priest", "goldfinger", "lindsey stirling", "sonic youth", 
    "gogol bordello", "kraddy", "phantom planet", "hatebreed", "wolfmother", "powerman 5000", 
    "george winston", "white stripes", "jason mraz", "junior senior", "james blunt", 
    "bob marley", "tangerine dream", "flyleaf", "sister sledge", "skism", "gordon lightfoot", 
    "nicki minaj", "the fray", "chris brown", "white zombie", "sum 41", "mr c", "keyshia cole", 
    "flaming lips", "blink 182", "sugarcult", "the fratellis", "new boyz", "kenny chesney", 
    "the lumineers", "deadmau5", "haddaway", "avicii", "rascal flatts", "jon pardi", 
    "lil wayne", "willie nelson", "eminem", "beck", "greg bates", "cherub", "leighton meester", 
    "buffalo springfield", "nadia ali", "miracle drug", "glee cast", "rusko", "indigo girls", 
    "eve 6", "gorillaz", "jefferson airplane", "krewella", "justin timberlake", "pantera", 
    "iron maiden", "christina perri", "casey james", "the remote", "zedd", "rob dougan", 
    "odetta", "citizen king", "pit bull", "coldplay", "prince royce", "bon jovi", "trace adkins","afrojack", "ratatat", "van halen", "sufjan stevens", "beastie boys", "m83", "muse", "berlin","train", "bloodhound gang", "gary allan", "miranda lambert", "calvin harris", "gwen stefani","godsmack", "grimes", "rolling stones", "generation x", "alex clare", "knife party", "stroke","morning parade", "chevelle", "bonnie tyler", "public enemy", "santana", "hollywood undead","tim mcgraw", "blaqk audio", "hugo", "snow patrol", "sneaker pimps", "drowning pool","duran duran", "lostprophets", "lacuna coil", "ed sheehan", "eric church", "freestylers","the killers", "daddy yankee", "django django", "cascada", "darius rucker", "pistol annies","tal bachman", "staind", "willow", "jeffree star", "beyonce", "major lazer", "stone sour","nelly furtado", "shania twain", "elliott smith", "smash mouth", "buckcherry", "mgmt", 
    "blackmill", "eric clapton", "lynyrd skynyrd", "deftones", "clutch", "dido", "chris cagle", 
    "matchbox twenty", "blind melon", "thompson square", "the cardigans", "marilyn manson", 
    "ozzy osborne", "randy houser", "amo ellas", "barenaked ladies", "don omar", "neon trees", 
    "jay z", "dire straits", "evanescence", "vertical horizon", "garvey", "jessie j", 
    "aqualung", "spice girls", "jeff buckley", "rem", "paul mccartney", "leo kottke", 
    "white town", "led zeppelin", "king crimson", "oasis", "bear mccreary", "ben folds", 
    "kristen kelly", "ok go", "metallica", "collective soul", "tomahawk", "estelle", 
    "bad brains", "disturbed", "the hives", "smashing pumpkins", "david archuleta", 
    "bon iver", "the smiths", "the beatles", "linkin park", "bjork", "grateful dead", 
    "james brown", "madeon", "imagine dragons", "miles davis", "genesis", "adventure club", 
    "kt tunstall", "postal service", "ellie goulding", "tool", "nirvana", "the cataracs", 
    "lcd soundsystem", "king missile", "clannad", "the skatalites", "frou fro", 
    "howlin wolf", "martin solveig", "pretty lights", "steve earle", "one direction", 
    "orgy", "muddy waters", "adam lambert", "trey anastasio", "candlebox", "velvet revolver", 
    "dan black", "peter gabriel", "brantley gilbert", "kacey musgraves", "adele", 
    "little dragon", "modest mouse", "luke bryan", "franz ferdinand", "sick puppies", 
    "foreigner", "the buggles", "the bled", "missy elliott", "the weeknd", "la roux", 
    "stabbing westward", "limp bizket", "everlast", "daughtry", "ac dc", "rancid", 
    "slipknot", "kip moore", "janis joplin", "good charlotte", "david guetta", 
    "reba mcentire", "queen", "eurythmics", "mutemath", "danny elfman", "volbeat", 
    "tenacious d", "enrique iglesias", "gotye", "alexander acha", "borgore", "rihanna", 
    "bush", "chopin", "fuel", "don mclean", "the byrds", "violent femmes", "leann rimes", 
    "oakenfold", "juicy j", "james taylor", "avenged sevenfold", "justin moore", 
    "citizen cope", "george strait", "porter robinson", "romeo santos", "the clash", 
    "dillon", "carlos vives", "bruce springsteen", "phil collins", "alanis morissette", 
    "sheryl crow", "soundgarden", "emmylou harris", "celtic woman", "bridget mendler", 
    "apollo 440", "the script", "toby keith", "motley crue", "neil young", "halestorm", 
    "brassica", "porcelain black", "apocolyptica", "foo fighters", "pearl jam", 
    "marcy playground", "lady sovereign", "black sabbath", "priestess", "kelly rowland", 
    "sublime", "no doubt", "harry chaplin", "lady antebellum", "placebo", "melanie fiona", 
    "the prodigy", "audioslave", "christina aguilera", "alicia keys", "alice cooper", 
    "the pretenders", "oingo boingo", "michael jackson", "gin blossoms", "imogen heap", 
    "jimi hendrix", "atrey", "china man", "lee brice", "asher roth", "the darkness", 
    "devotchka", "sevendust", "alexandra stan", "billy joel", "timbaland", "moody blues", 
    "frank zappa", "savage garden", "nickelback", "massive attack", "benny benassi", 
    "the bravery", "onerepublic", "the wanted", "jack white", "die antwood", "styx", 
    "soil", "sting", "kelly clarkson", "butthole surfers", "the who", "madonna", 
    "flogging molly", "rob thomas", "tony bennett", "jawbreaker", "tim mcmorris", 
    "semisonic", "rob zombie", "ween", "blake shelton", "everclear", "carrie underwood", 
    "cassadee pope", "lou bega", "stateless", "jake owens", "moby", "pitbull", 
    "alejandro sanz", "bassnecter", "lightning bolt", "peeping tom", "ciara", 
    "blue foundation", "parov stelar", "bob dylan", "50 cent", "portishead", 
    "sugar ray", "breaking benjamin", "darude", "eric prydz", "steely dan", 
    "adema", "def leppard", "beach boys", "newcleus", "lovage", "jethro tull", 
    "laura gibson", "the cure", "crystal castles", "depeche mode", "creed", 
    "lena", "crazy town", "usher", "incubus", "zero 7", "radiohead", "shakira", 
    "lifehouse", "bruno mars", "amanda brown", "the used", "chainz", "dustin lynch", 
    "joy division", "hinder", "lmfao", "papa roach", "skrillex", "akon", "aerosmith", 
    "eiffel 65", "silversun pickups", "owl city", "flux pavilion", "fleetwood mac", 
    "ben howard", "the dreaming", "disclosure", "garbage", "trust company", 
    "britney spears", "eighteen visions", "thomas newman", "tracy chapman", 
    "cobra starship", "pink floyd", "jason derulo", "tantric", "don davis", 
    "green day", "jason aldean", "kylie minogue", "nashville cast", "madilyn bailey", 
    "cher lloyd", "melanie martinez", "gnarls barkley", "symphony x", "awolnation", 
    "seether", "pinkly smooth", "easton corbin", "rudimental", "hunter hayes", "fiona apple", 
    "counting crows", "purity ring", "chromeo", "sbtrkt", "the vines", "sex pistols", 
    "ghost town", "cake", "jose feliciano", "daft punk", "kid rock", "lady gaga", "monsta", 
    "nero", "teenage days", "bingo players", "shinedown", "french montana", "justin bieber", 
    "korn", "david bowie", "george gershwin", "otto knows", "enya", "jennifer lopez", 
    "mike posner", "bag raiders", "icona pop", "the offspring", "rita ora", "thomas rhett", 
    "the misfits"]
    return render_to_response('bandlistens.html', {"bands": json.dumps(band_json)},context_instance=RequestContext(request))


# #commented out so that the requests don't get accidentally fired
# def fips(request):
#     for county in County.objects.all():
#         if len(county.fips) == 3:
#             county.fips = county.state.fips + county.fips
#             county.save()
#     return render_to_response('index.html', {},context_instance=RequestContext(request))

# def bcc(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/banded_county_count.txt')), 'r') as bcc:
#         for line in bcc:
#             bcc_line = line.split(',')

#             county = bcc_line[2]
#             state = bcc_line[1]
#             count = int(bcc_line[3])

#             saint = county[0:3]
#             city_par = county[-6:]
#             miami = county[0:5]

#             if city_par == "(City)":
#                 county = county[:-7] + " city"

#             if county == "Dekalb" and not state == "MO" and not state == "TN":
#                 county = "De Kalb"

#             if not state == "ON" and not state == "BC" and not state == "BC" and not state == "QC":
#                 county = county.lower()
#                 try:
#                     fips = Fips.objects.get(county=county.replace("'", ""), state=bcc_line[1])
#                     band_name = bcc_line[0]
#                     # print fips.state_fips + fips.county_fips
#                     county_obj = County(name=county, fips=fips.state_fips + fips.county_fips,count=count)
#                     try:
#                         band = Band.objects.get(name=band_name)
#                         band.counties.append(county_obj)
#                         band.save()
#                     except:
#                         band = Band(name=band_name)
#                         band.counties.append(county_obj)
#                         band.save()
#                 except:
#                     print county + " " + state
                        
#     return render_to_response('index.html', {},context_instance=RequestContext(request)) 

# def bsc(request):
#     states = ["AL","AK", "AZ","AR","CA",
#"CO","CT","DE","FL","GA","HI","ID",
#             "IL","IN","IA","KS","KY","LA","ME","MD",
#             "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC",
#             "ND","OH","OK","OR","PA","RI",
#"SC","SD","TN","TX","UT","VT",
#             "VA","WA","WV","WI","WY"]
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/banded_state_count.txt')), 'r') as bsc:
#         for line in bsc:
#             bsc_line = line.split(',')
#             band_name = bsc_line[0]
#             state = bsc_line[1]
#             count = int(bsc_line[2])
#             state_obj = State(name=state, count=count)
#             if state in states:
#                 try:
#                     band = Band.objects.get(name=band_name)
#                     band.states.append(state_obj)
#                     band.save()
#                 except:
#                     print "failed"
#     return render_to_response('index.html', {},context_instance=RequestContext(request))         



# def getfips(request):
#     county = request.GET['county'].lower().replace(" ", "")
#     state = request.GET['state']
#     try:
#         fips = Fips.objects.get(county=county, state=state)
#         response = {"response": "success", "fips": fips.county_fips}
#         return HttpResponse(json.dumps(response), mimetype="application/json")
#     except:
#         response = {"response": "failure"}
#         return HttpResponse(json.dumps(response), mimetype="application/json")


# def topstate(request):
#     state_name = request.GET['state'].upper()
#     bands = Band.objects.raw_query({"states.name" : state_name})
#     response = {}
#     for band in bands:
#         for state in band.states:
#             if state.name == state_name:
#                 response[band.name] = state.count
#     sorted_response = sorted(response.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]
#     return HttpResponse(json.dumps(sorted_response), mimetype="application/json")


# def state(request):
#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/fipsstates.txt')), 'r') as fips:
#         for line in fips:
#             print line
#             fips_line = line.split(',')
#             # print fips_line[0] + " "  +fips_line[3]
#             state = State(name=fips_line[1],fips=fips_line[0],abbr=fips_line[2])
#             state.save()

#     return render_to_response('index.html', {},context_instance=RequestContext(request))




