#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas 
import matplotlib.pyplot as plt
from geopy.geocoders import GoogleV3, Nominatim
from stream_tweets import getTweetJSON

class geoDF:
    def __init__(self):
        self.tweetjson = getTweetJSON()
        self.df = getUserFeatures(self.tweetjson)
        

    ## DF Apply Funs ###
    def getUserFeatures(tweets_json):
        "foo foo foo, bar bar bar"
        tweets_df = pandas.DataFrame()
        tweets_df['user_id'] = map(lambda tweet: str(tweet['user']['id'])\
                            if 'user' in tweet.keys() \
                            else None, tweets_json)
        tweets_df['name'] = map(lambda tweet: tweet['user']['name']\
                            if 'user' in tweet.keys() \
                            else None, tweets_json)

        tweets_df['verified'] = map(lambda tweet: tweet['user']['verified'] * 1\
                                    if 'user' in tweet.keys()\
                                    else None, tweets_json)
        tweets_df['description'] = map(lambda tweet: tweet['user']['description']\
                if 'user' in tweet.keys() \
                else None, tweets_json)

        tweets_df['followers_ct'] = map(lambda tweet: tweet['user']['followers_count'] \
                if 'user' in tweet.keys() \
                else None, tweets_json)
        
        tweets_df['friends_ct'] = map(lambda tweet: tweet['user']['friends_count']\
                if 'user' in tweet.keys() \
                else None, tweets_json)

        tweets_df['statuses_ct'] = map(lambda tweet: tweet['user']['statuses_count']\
                if 'user' in tweet.keys() \
                else None, tweets_json)


        return tweets_df


    """
    def filterByUSA(geo_df):
        "Use googles geocoding API" 
        # places with US time zone:
        geo_df['countryUSA'] = geo_df.country.apply(lambda row: row == "United States"\
                                                if row else None, 1)
        geo_df['tzUSA'] = geo_df.apply(lambda row: filterTz(row.time_zone) \
                                                if row.countryUSA == None and \
                                                row.time_zone else None, 1)
        geo_df['locatUSA'] = geo_df.apply(lambda row: filterLocat(row.location) \
                                            if (row.countryUSA == None) & (row.tzUSA == None)\
                                            and row.location else None, 1)

        usa_df  = geo_df[(geo_df.countryUSA == True) | \
                            (geo_df.tzUSA == True) | \
                            (geo_df.locatUSA == True)]
        return geo_df, usa_df
        """
    
## Helpers ##
def getAddress(locat):
    #geolocat = GoogleV3()
    geolocat = Nominatim()
    geo = None
    try:
        geo = geolocat.geocode(locat)
    except Exception as e:
        print e
        return None
    if geo:
        return geo.address

def filterTz(tz):
    """Check if timezone in USA"""
    US_tz = ["Alaska", "Hawaii", "Pacific/Honolulu", "Pacific Time (US & Canada)",\
            "Mountain Time (US & Canada)", "Central Time (US & Canada)",\
            "Eastern Time (US & Canada)"]
    return tz in US_tz

def filterLocat(locat):
    """Check if geocode in USA"""
    geolocat = Nominatim()
    try:
        geo = geolocat.geocode(locat)
        if geo:
            return "United States" in geo.address 
        else:
            return None
    except:
        return None

if __name__ == '__main__':
    pass
