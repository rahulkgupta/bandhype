# Quinn's twitter aggregator that filters twitter streams based on #Spotify and #Rdio tags.

import tweepy
import sys
import webbrowser
import codecs
import re
import simplejson
from time import gmtime, strftime
import json
import urllib

auth = tweepy.auth.OAuthHandler('FoXQACe6NWrvKcgGAqFaLQ','xrNqpix1tW4MY0ESBP3PnYx7i7vvAzfU6DT4X97d0I')
auth.set_access_token('573006802-TCFG3dJ1tviqLAeXoo0FdQ4VB5U8dlptP1Av74EV','Cmt0VLnmwCmXY5ozWDaXfdiXuI0n0UROZKIPkWjtk')
api = tweepy.API(auth)

MapQuest_API_KEY = """Fmjtd%7Cluuanua7n0%2C85%3Do5-96b054"""

#this makes sure that the name of the name of the file has the timestamp to prevent overwriting past datasets
timeString = strftime("listen_%a_%d%b%Y_%Hh%Mm%Ss_GMT", gmtime())
fileObj = codecs.open(timeString+'.txt','w','utf-8') #open a UTF-8 file to write to

patTab = re.compile(r'[^(!-~)]') #this regular expression removes tabs from the status.text
patNewLine = re.compile(r'\n+') #this regular expression removes new line characters from the status.text

#the string listener below is based losely upon that described at the URL below
#http://answers.oreilly.com/topic/2605-how-to-capture-tweets-in-real-time-with-twitters-streaming-api/
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            # print (status.text, status.coordinates, status.place, status.user.location)
            captured = True
            tweet_meat = ""
            # fileObj.write(status.text + "\n")
            status.text = clean_tweet(status.text)

            # Example tweet: Listening to "Feel This Moment" by Pitbull on @Rdio: http://t.co/DkkBRFgV hell yeahhh
            if "Listening to" in status.text and " by" in status.text and " on @Rdio" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on @Rdio")]

            # Example tweet: I'm listening to "Makin' Good Love" by Avant on Pandora http://t.co/BM6CCP55 #pandora
            elif "listening to" in status.text and " by" in status.text and " on Pandora" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" on Pandora")]

            elif "Listening to" in status.text and " by" in status.text and " on exfm" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on exfm")]

            # Example tweet: Listening to shutDOWN by OSI #nowplaying  http://t.co/CwdXcWYO via @grooveshark
            elif "Listening to" in status.text and " by" in status.text and " via @grooveshark" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" #nowplaying")]

            # Example tweet: listening to Tan solo un beso tuyo by Guaco on @Grooveshark: http://t.co/lALpl3lL #nowplaying
            elif "listening to" in status.text and " by" in status.text and " on @Grooveshark" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on @Grooveshark")]

            # Example tweet: I'm listening to "In The Morning" by Michal Menert (on The World of Pretty Lights) http://t.co/Q7D7vYjj via the @Songza iPhone app
            elif "listening to" in status.text and " by" in status.text and " via the @Songza" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" (on")]

            # Example tweet: I'm listening to Warwick Avenue by Duffy http://t.co/LZPXzjBG via @lastfm
            elif "listening to" in status.text and " by" in status.text and " via @lastfm" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" http:")]

            # Example tweet: Listening to: - I Want Your Love by Chic, from #SoundHound http://t.co/0z50CaP8
            # Note, the "-" is really a \xe2\x80\x93 character that is filtered out by clean_tweet.
            elif "Listening to" in status.text and " by" in status.text and ", from #SoundHound" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 16:(status.text).rindex(", from #SoundHound")]

            # Example tweet: Listening to HydROlics by M.E ft. A.Love (Explicit) @hulkshare -  http://t.co/qPJJySlx
            elif "Listening to" in status.text and " by" in status.text and " @hulkshare" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" @hulkshare")]

            # Example tweet: Listening to "How To Be a Werewolf (Xander Harris Remix)" by Mogwai #nowplaying #track8app
            elif "Listening to" in status.text and " by" in status.text and " #nowplaying #track8app" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" #nowplaying #track8app")]

            # Example tweet: I'm listening to U Are My Fantasy [Street Fighter II Theme Remix] by Zomby using @doubleTwist http://t.co/WLlYl02N
            elif "listening to" in status.text and " by" in status.text and " using @doubleTwist" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" using @doubleTwist")]

            # Example tweet:  Listening to 'Rain Forest (reprise)' by 'Bobby Lyle'  #iTweetMyTunes
            elif "Listening to" in status.text and " by" in status.text and "  #iTweetMyTunes" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex("  #iTweetMyTunes")]

            else:
                captured = False
                
            if captured == True:
                # Testing Code
                captured_info = {"song_title": clean_song_title(tweet_meat[:tweet_meat.rindex(" by")]), "artist_name": clean_artist_name(tweet_meat[tweet_meat.rindex(" by") + 4:])}
                # fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")
                # fileObj.write(str(status.coordinates) + "\t" + str(status.place) + "\t" + str(status.user.location) + "\t" + str(getLocation(status)) + "\n")
                lonlat = getLocation(status)
                fileObj.write(str(captured_info["artist_name"]) + "\t" + str(status.author.screen_name) + "\t" + str(lonlat[0]) + "\t" + str(lonlat[1]) + "\t" + str(status.created_at) + "\t" + str(status.text) + "\n")
            # fileObj.write("\n")

            # reformattedStatus1 = patTab.sub(' ', status.text)
            # reformattedStatus2 = patNewLine.sub(' ', reformattedStatus1)
            # jsonCoordinates = status.coordinates
            # jsonPlace = status.place

            # if status.coordinates == None:
            #     txtCoordinates = 'None'
            # else:
            #     txtCoordinates = jsonCoordinates.get('coordinates', None)

            # print '-------------------------------\n%s\t%s\t%s' % (status.author.screen_name, txtCoordinates, reformattedStatus2)
            # fileObj.write(  status.author.screen_name+'\t'
            #         +str(txtCoordinates)+'\t'
            #         +str(status.created_at)+'\t'
            #         +reformattedStatus2)
            # fileObj.write("\n")

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def clean_tweet(tweet):
        cleaned_tweet = tweet.replace("&amp;", "&")
        cleaned_tweet = cleaned_tweet.replace("\n", "")
        cleaned_tweet = re.sub(r'[^( -~)]', "", cleaned_tweet) # replaces any odd characters with ""
        return cleaned_tweet

def clean_song_title(title):
    cleaned_title = title.replace("'", "").replace('"', "").lower()
    return cleaned_title

def clean_artist_name(name):
    cleaned_artist = name.replace("'", "").replace('"', "").replace("@", "").lower()
    return cleaned_artist

#returns lnglat pair in list format.
def getLocation(status):
    lnglat = None
    if status.coordinates != None:
        lnglat = status.coordinates["coordinates"]
    elif status.place != None:
        place_name = status.place["full_name"]
        api_call = "http://www.mapquestapi.com/geocoding/v1/address?key=" + str(MapQuest_API_KEY) + "&location=" + str(place_name)
        response = urllib.urlopen(api_call).read()
        response_JSON = json.loads(response)
        longitude = response_JSON["results"][0]["locations"][0]["latLng"]["lng"]
        latitude = response_JSON["results"][0]["locations"][0]["latLng"]["lat"]  
        lnglat = [float(longitude), float(latitude)]
    else:
        user_location = str(status.user.location)
        if user_location != "":
            api_call = "http://www.mapquestapi.com/geocoding/v1/address?key=" + str(MapQuest_API_KEY) + "&location=" + str(user_location)
            response = urllib.urlopen(api_call).read()
            response_JSON = json.loads(response)
            if (response_JSON["results"][0]["locations"][0]["adminArea1"] == "US") and (response_JSON["results"][0]["locations"][0]["geocodeQuality"] == "CITY"):   
                longitude = response_JSON["results"][0]["locations"][0]["latLng"]["lng"]
                latitude = response_JSON["results"][0]["locations"][0]["latLng"]["lat"]  
                lnglat = [float(longitude), float(latitude)]
                if lnglat[0] == float(-99.141968) and lnglat[1] == float(39.527596):
                    lnglat = None
    return lnglat

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout = 90)
earth=[-180,-90,180,90]
fortyEightStates=[-125.0,24.5,-66.5,49.5]
# streaming_api.filter(locations = fortyEightStates)
streaming_api.filter(track = ["@Rdio", "Listening to by"])