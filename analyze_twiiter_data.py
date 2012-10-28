import sys
import ast
import codecs

def get_band_data():
    list_of_bands =[]
    with open('bandnames.txt', 'r') as fbands:
        for line in fbands:
            list_of_bands.append(line.rstrip().lower())
    return list_of_bands

def analyse_tweet_data(datafile):
    banddata = get_band_data()
    print banddata
    with open(datafile, 'r') as ftweets:
        for line in ftweets:
            tweet_line = line.split('\t')
	    # parsed the line for future processing
            user_name = tweet_line[0]
            coordinate_list =ast.literal_eval(tweet_line[1])
            tweet_time = tweet_line[2]
            tweet_text = tweet_line[3].lower()
            #print tweet_text
            for band in banddata:
		try:
		    if str(band) in tweet_text:
			fileWrite.write(band +'\t' +line +'\n')
			#fileWrite.write(line)
			#fileWrite.write("\n")
			print '%s\t%s'%(band,tweet_text)
		except:
		    # Catch any unicode errors while printing to console
		    # and just ignore them to avoid breaking application.
		    pass


fileWrite = codecs.open('band_'+sys.argv[1].split('.')[0]+'.txt','w','utf-8')
analyse_tweet_data(sys.argv[1])


