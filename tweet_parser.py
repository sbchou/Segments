#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas 
import matplotlib.pyplot as plt
"""
Simple code to collect sample of public tweets.
"""

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'

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

def tweetsToPD(tweets_json):
    tweets_df = pandas.DataFrame()
    tweets_df['text'] = map(lambda tweet: tweet['text']\
                         if 'text' in tweet.keys()\
                        else None, tweets_json)
    tweets_df['lang'] = map(lambda tweet: tweet['lang']\
                        if 'lang' in tweet.keys() else None, tweets_json)
    tweets_df['country'] = map(lambda tweet: tweet['place']['country'] \
                        if 'place' in tweet.keys() and tweet['place'] != None\
                         else None, tweets_json)
    return tweets_df

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
