#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas 
import matplotlib.pyplot as plt
from geopy.geocoders import GoogleV3, Nominatim
"""
Simple code to collect sample of public tweets.
"""

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'

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

class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status
    
    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def printStream():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    stream = Stream(auth, l)
    stream.sample()
    #stream.filter(track=['python', 'javascript', 'ruby'])


def loadTweets(tweets_json_path='data/stream_test.txt'):
    tweets_json = []
    tweets_file = open(tweets_json_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_json.append(tweet)
        except:
            continue
    return tweets_json

def tweetsToDF(tweets_json):
    tweets_df = pandas.DataFrame()
    #cast id to a string, or else it truncates it into a 17 digit float
    tweets_df['id'] = map(lambda tweet: str(tweet['id'])\
                        if 'id' in tweet.keys()\
                        else None, tweets_json)
    tweets_df['text'] = map(lambda tweet: tweet['text']\
                         if 'text' in tweet.keys()\
                        else None, tweets_json)
    tweets_df['lang'] = map(lambda tweet: tweet['lang']\
                        if 'lang' in tweet.keys() else None, tweets_json)
    tweets_df['country'] = map(lambda tweet: tweet['place']['country'] \
                        if 'place' in tweet.keys() and tweet['place'] != None\
                         else None, tweets_json)
    return tweets_df

def getGeoInfo(tweets_json):
    "try to get all location predictors"
    tweets_df = pandas.DataFrame()
    tweets_df['id'] = map(lambda tweet: str(tweet['id'])\
                        if 'id' in tweet.keys()\
                        else None, tweets_json)
    tweets_df['time_zone'] = map(lambda tweet: tweet['user']['time_zone']\
                                if 'user' in tweet.keys() else None, tweets_json)
    tweets_df['lang'] = map(lambda tweet: tweet['lang']\
                        if 'lang' in tweet.keys() else None, tweets_json)
    tweets_df['country'] = map(lambda tweet: tweet['place']['country'] \
                        if 'place' in tweet.keys() and tweet['place'] != None\
                         else None, tweets_json)
    tweets_df['location'] = map(lambda tweet: tweet['user']['location'] \
                        if 'user' in tweet.keys() else None, tweets_json)
    tweets_df['geo'] = map(lambda tweet: tweet['geo']['coordinates']\
                        if 'geo' in tweet.keys() \
                        and tweet['geo'] != None\
                        else None, tweets_json)
    return tweets_df

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


def filterTz(tz):
    """Check if timezone in USA"""
    US_tz = ["Alaska", "Hawaii", "Pacific/Honolulu", "Pacific Time (US & Canada)",\
            "Mountain Time (US & Canada)", "Central Time (US & Canada)",\
            "Eastern Time (US & Canada)"]
    return tz in US_tz


def plotByLang(tweets_df):
    tweets_by_lang = tweets_df['lang'].value_counts()

    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('figs/tweets_by_lang.png')



def plotByCountry(tweets_df):
    tweets_by_country = tweets_df['country'].value_counts()

    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
    plt.savefig('figs/tweets_by_country.png')





if __name__ == '__main__':
    printStream()
