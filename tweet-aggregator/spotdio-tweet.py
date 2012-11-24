# Quinn's twitter aggregator that filters twitter streams based on #Spotify and #Rdio tags.

import tweepy
import sys
import webbrowser
import codecs
import re
import simplejson
from time import gmtime, strftime

auth = tweepy.auth.OAuthHandler('FoXQACe6NWrvKcgGAqFaLQ','xrNqpix1tW4MY0ESBP3PnYx7i7vvAzfU6DT4X97d0I')
auth.set_access_token('573006802-TCFG3dJ1tviqLAeXoo0FdQ4VB5U8dlptP1Av74EV','Cmt0VLnmwCmXY5ozWDaXfdiXuI0n0UROZKIPkWjtk')
api = tweepy.API(auth)

#this makes sure that the name of the name of the file has the timestamp to prevent overwriting past datasets
timeString = strftime("%a_%d%b%Y_%Hh%Mm%Ss_GMT", gmtime())
fileObj = codecs.open(timeString+'.txt','w','utf-8') #open a UTF-8 file to write to

patTab = re.compile(r'[^(!-~)]') #this regular expression removes tabs from the status.text
patNewLine = re.compile(r'\n+') #this regular expression removes new line characters from the status.text

#the string listener below is based losely upon that described at the URL below
#http://answers.oreilly.com/topic/2605-how-to-capture-tweets-in-real-time-with-twitters-streaming-api/
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            fileObj.write(status.text + "\n")
            status.text = clean_tweet(status.text)

            # Example tweet: Listening to "Feel This Moment" by Pitbull on @Rdio: http://t.co/DkkBRFgV hell yeahhh
            if "Listening to" in status.text and " by" in status.text and " on @Rdio" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on @Rdio")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: I'm listening to "Makin' Good Love" by Avant on Pandora http://t.co/BM6CCP55 #pandora
            elif "listening to" in status.text and " by" in status.text and " on Pandora" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" on Pandora")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            elif "Listening to" in status.text and " by" in status.text and " on exfm" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on exfm")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: Listening to shutDOWN by OSI #nowplaying  http://t.co/CwdXcWYO via @grooveshark
            elif "Listening to" in status.text and " by" in status.text and " via @grooveshark" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" #nowplaying")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: listening to Tan solo un beso tuyo by Guaco on @Grooveshark: http://t.co/lALpl3lL #nowplaying
            elif "listening to" in status.text and " by" in status.text and " on @Grooveshark" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" on @Grooveshark")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: I'm listening to "In The Morning" by Michal Menert (on The World of Pretty Lights) http://t.co/Q7D7vYjj via the @Songza iPhone app
            elif "listening to" in status.text and " by" in status.text and " via the @Songza" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" (on")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")
            # Example tweet: I'm listening to Warwick Avenue by Duffy http://t.co/LZPXzjBG via @lastfm
            elif "listening to" in status.text and " by" in status.text and " via @lastfm" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" http:")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: Listening to: - I Want Your Love by Chic, from #SoundHound http://t.co/0z50CaP8
            # Note, the "-" is really a \xe2\x80\x93 character that is filtered out by clean_tweet.
            elif "Listening to" in status.text and " by" in status.text and ", from #SoundHound" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 16:(status.text).rindex(", from #SoundHound")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: Listening to HydROlics by M.E ft. A.Love (Explicit) @hulkshare -  http://t.co/qPJJySlx
            elif "Listening to" in status.text and " by" in status.text and " @hulkshare" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" @hulkshare")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: Listening to "How To Be a Werewolf (Xander Harris Remix)" by Mogwai #nowplaying #track8app
            elif "Listening to" in status.text and " by" in status.text and " #nowplaying #track8app" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex(" #nowplaying #track8app")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet: I'm listening to U Are My Fantasy [Street Fighter II Theme Remix] by Zomby using @doubleTwist http://t.co/WLlYl02N
            elif "listening to" in status.text and " by" in status.text and " using @doubleTwist" in status.text:
                tweet_meat = status.text[(status.text).rindex("listening to") + 13:(status.text).rindex(" using @doubleTwist")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            # Example tweet:  Listening to 'Rain Forest (reprise)' by 'Bobby Lyle'  #iTweetMyTunes
            elif "Listening to" in status.text and " by" in status.text and "  #iTweetMyTunes" in status.text:
                tweet_meat = status.text[(status.text).rindex("Listening to") + 13:(status.text).rindex("  #iTweetMyTunes")]
                captured_info = {"song_title": tweet_meat[:tweet_meat.rindex(" by")].replace('"', "").replace("'", ""), "artist_name": tweet_meat[tweet_meat.rindex(" by") + 4:].replace("@","").replace("'", "")}
                fileObj.write("Captured! Song: {song_title}, Artist: {artist_name}".format(**captured_info) + "\n")

            fileObj.write("\n")

            # print(status.author.screen_name, status.coordinates, status.text, status.place, status.user.location, status.user.geo_enabled)
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

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout = 90)
earth=[-180,-90,180,90]
fortyEightStates=[-125.0,24.5,-66.5,49.5]
streaming_api.filter(track = ["@Rdio", "Listening to by"])