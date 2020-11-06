#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: OstermannFO

TwitterStream_AWS_London.py: 
    access TwitterStreamingAPI
    query all geolocated Tweets in GLA
    write Tweets as JSON objects in text file
    
currently still using Python2; 
"""

import twitter
import io
import json
import time

# set query parameters
TRACK = '' #Comma-separated list of terms
LOCATIONS = '-0.489,51.28,0.236,51.686' #bounding box

# set path to output files
OUTPUT_PATH = '/path/to/output/files/'

# add authentification details 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
    
def oauth_login():   
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

    
def save_json(filename, data):    
    with io.open('{}{}.txt'.format(OUTPUT_PATH, filename),
                 'a', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False))+'\n')


def main():    
    twitter_api = oauth_login()          
    filename = time.strftime("%Y%m%d-%H%M%S")    
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)    
    twitter_tweets = twitter_stream.statuses.filter(track=TRACK,
                                                   locations=LOCATIONS)    
    for tweet in twitter_tweets:
        save_json(filename, tweet)

if __name__=="__main__":
    main()        