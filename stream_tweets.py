#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas 
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


def getTweetJSON(tweets_json_path='data/stream_test.txt'):
    tweets_json = []
    tweets_file = open(tweets_json_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_json.append(tweet)
        except:
            continue
    return tweets_json

if __name__ == '__main__':
    printStream()
