#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pymongo import MongoClient
"""
Simple code to 
"""

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'

class StdOutListener(StreamListener):

    def on_data(self, data): 
        client = MongoClient('localhost', 27017)
        db = client['twitter_db']
        collection = db['twitter_collection']
        tweet = json.loads(data)

        collection.insert(tweet)

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


if __name__ == '__main__':
    printStream()
