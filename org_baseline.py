#Import the necessary methods from tweepy library
import twitter
import json
import pandas 
import matplotlib.pyplot as plt
from geopy.geocoders import GoogleV3, Nominatim
from stream_tweets import getTweetJSON

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'
api = twitter.Api(consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)
#last 100 twts
# stati = api.GetUserTimeline('1506671', count=100)
class geoDF:
    def __init__(self):
        self.tweetjson = getTweetJSON()
        self.training = getTraining() 
        self.features = getUserFeatures(self.training)
1
    ## DF Apply Funs ###
    def getUserFeatures(training):
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
        
    def getTraining(path='data/humanizr_data/humanizr_labeled.tsv'):
        training = pandas.DataFrame.from_csv(path, sep="\t")

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
