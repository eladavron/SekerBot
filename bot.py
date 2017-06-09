import tweepy
import configparser
import re
import os
import sys
import logging
import traceback
from bidi import algorithm
from pathlib import Path

#Get latest post time
configPath = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
config = configparser.ConfigParser()
config.read(configPath)
last_id = int(config.get('main', 'last_id'))

#Check if tokens are available
def GetAuth():
    try:
        from tokens import api_key, api_secret, access_token, access_token_secret
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    except ModuleNotFoundError as mex:
        print('Tokens not defined! Running onetime authenticator...')
        import onetime
        return GetAuth()
    except Exception as ex:
        print('Something unknown happened')
        return

def RetweetSekers(last_id):
    api = GetAuth()
    tweets = api.search('#סקר', lang="he", since_id=last_id)
    for tweet in tweets:
        if tweet.user != api.me:
            if tweet.id > last_id:
                last_id = tweet.id
            try:
                api.retweet(tweet.id)
                print('Retweeted: ' +  MessageUrlBuilder(tweet))
                print(algorithm.get_display(tweet.text))
            except tweepy.TweepError as ex:
                if ex.api_code == 327:
                    #print('Already retweeted: ' + MessageUrlBuilder(tweet))
                    pass
                else:
                    logging.error(traceback.format_exc())
        SaveLastID(last_id)

def MessageUrlBuilder(status):
    return 'https://www.twitter.com/' + status.user.screen_name + '/status/' + str(status.id)

def SaveLastID(last_id):
    config['main']['last_id'] = str(last_id)
    with open(configPath, 'w') as configWriter:
        config.write(configWriter)

RetweetSekers(last_id)
quit()
