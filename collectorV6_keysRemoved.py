# David Adamson's twitter stream downloader

import tweepy
import sys
import webbrowser
import codecs
import re
import simplejson
from time import gmtime, strftime

auth = tweepy.auth.OAuthHandler('','')
auth.set_access_token('','')
api = tweepy.API(auth)

#this makes sure that the name of the name of the file has the timestamp to prevent overwriting past datasets
timeString = strftime("%a_%d%b%Y_%Hh%Mm%Ss_GMT", gmtime())
fileObj = codecs.open(timeString+'.txt','w','utf-8') #open a UTF-8 file to write to

patTab = re.compile(r'\t+') #this regular expression lets me remove tabs from the status.text
patNewLine = re.compile(r'\n+') #this regular expression lets me remove tabs from the status.text

#the string listener below is based losely upon that described at the URL below
#http://answers.oreilly.com/topic/2605-how-to-capture-tweets-in-real-time-with-twitters-streaming-api/
class CustomStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		try:
			reformattedStatus1 = patTab.sub(' ', status.text)
			reformattedStatus2 = patNewLine.sub(' ', reformattedStatus1)
			jsonCoordinates = status.coordinates
			jsonPlace = status.place

			if status.coordinates == 'None':
				txtCoordinates = 'None'
			else:
				txtCoordinates = jsonCoordinates.get('coordinates', None)

			print '-------------------------------\n%s\t%s' % (status.author.screen_name, txtCoordinates,)
			fileObj.write(	status.author.screen_name+'\t'
					+str(txtCoordinates)+'\t'
					+str()+'\t'
					+str(status.created_at)+'\t'
					+reformattedStatus2)
			fileObj.write("\n")

		except Exception, e:
			print >> sys.stderr, 'Encountered Exception:', e
			pass

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
	        print >> sys.stderr, 'Timeout...'
	        return True # Don't kill the stream

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout = 90)
earth=[-180,-90,180,90]
fortyEightStates=[-125.0,24.5,-66.5,49.5]
streaming_api.filter(locations = fortyEightStates)

