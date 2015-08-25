#Import the necessary methods from tweepy library
import twitter
import json
import pandas 
import matplotlib.pyplot as plt
from geopy.geocoders import GoogleV3, Nominatim
import csv
from progressbar import ProgressBar
import random
from twitter import TwitterError
import time

def init_twitt():
    CONSUMER_KEY = 'RE9RJs5c3zQ8yhLCZQCKlVglT'
    CONSUMER_SECRET = 'iA5ElxRl9JWm4wYDntSI2UxT56Yp6SpcDkAJ40EoDvMMFnWkfK'
    ACCESS_KEY = '359150678-DAyroyYOpYkqLiCaNIok2M9KoY2fj1C4fxBO5v6R'
    ACCESS_SECRET = 'zhTmAekrR0hcX4yfV4mRLVx1OQZMuIikj3dTvtfzghjAZ'
    api = twitter.Api(consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)
    return api

def getTraining(path='data/humanizr_data/humanizr_labeled.tsv'):
    training = pandas.DataFrame.from_csv(path, sep="\t")
    return training

def getUserFeatures(training, api):
    with open('data/userfeatures.csv', 'wt') as f:
        pbar = ProgressBar()
        writer = csv.writer(f)
        writer.writerow(("id", "screenname", "name", "verified",\
                "desc", "favorites_ct", "followers_ct", \
                "friends_ct", "tweets_ct"))
        n = len(training.index)
        ids = list(training.index)
        random.shuffle(ids)
        again = True
        for t_id in pbar(ids):
            while again == True:
                try:
                    user = api.GetUser(t_id)
                    screenname = user.GetScreenName()
                    name = user.GetName()
                    verified = user.GetVerified()
                    description = user.GetDescription()
                    favorites_ct = user.GetFavouritesCount()
                    followers_ct = user.GetFollowersCount()
                    friends_ct = user.GetFriendsCount()
                    tweets_ct = user.GetStatusesCount()
                    writer.writerow([unicode(s).encode("utf-8") for s in (t_id, screenname, name, verified, \
                            description, favorites_ct, followers_ct, \
                            friends_ct, tweets_ct)])
                    print "done", t_id
                    again = False
                except TwitterError:
                    print t_id, "zzZZZZZz"
                    time.sleep(5)
                    again = True
                except Exception, e:
                    import pdb; pdb.set_trace()
                    print str(e)

def runFeatureExtract():
    """Outputs the feature + label CSV"""
    api = init_twitt()
    training = getTraining()
    getUserFeatures(training, api)

def joinLabels(LABEL_PATH='data/humanizr_data/humanizr_labeled.tsv',\
                FEATURE_PATH='data/userfeatures.csv'):
    labels = pandas.DataFrame.from_csv(LABEL_PATH, sep="\t")
    features = pandas.DataFrame.from_csv('data/userfeatures.csv')
    joined = features.join(labels)
    joined = joined[np.isfinite(joined['type'])]
    joined['verified'] = joined['verified'] * 1 # binarize
    joined.to_csv('data/labeled_features.csv')
    joined[['verified', 'favorites_ct', 'followers_ct', 'friends_ct',\
            'tweets_ct','type']].to_csv('data/baseline_feats.csv')

if __name__ == '__main__':
    runFeatureExtract()