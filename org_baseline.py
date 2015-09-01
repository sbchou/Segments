import tweepy
import json
import pandas 
import matplotlib.pyplot as plt
from geopy.geocoders import GoogleV3, Nominatim
import csv
from progressbar import ProgressBar
import random
from tweepy import TweepError
import time
import numpy as np
import sklearn
import frogress
from pymongo import MongoClient

def init_twitt():
    CONSUMER_KEY = 'RE9RJs5c3zQ8yhLCZQCKlVglT'
    CONSUMER_SECRET = 'iA5ElxRl9JWm4wYDntSI2UxT56Yp6SpcDkAJ40EoDvMMFnWkfK'
    #ACCESS_KEY = '359150678-DAyroyYOpYkqLiCaNIok2M9KoY2fj1C4fxBO5v6R'
    #ACCESS_SECRET = 'zhTmAekrR0hcX4yfV4mRLVx1OQZMuIikj3dTvtfzghjAZ'
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth)
    return api

def init_json_api():
    CONSUMER_KEY = 'RE9RJs5c3zQ8yhLCZQCKlVglT'
    CONSUMER_SECRET = 'iA5ElxRl9JWm4wYDntSI2UxT56Yp6SpcDkAJ40EoDvMMFnWkfK'
    #ACCESS_KEY = '359150678-DAyroyYOpYkqLiCaNIok2M9KoY2fj1C4fxBO5v6R'
    #ACCESS_SECRET = 'zhTmAekrR0hcX4yfV4mRLVx1OQZMuIikj3dTvtfzghjAZ'
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())
    return api

def getTraining(path='data/humanizr_data/humanizr_labeled.tsv'):
    training = pandas.DataFrame.from_csv(path, sep="\t")
    return training

def saveUsers(training, api):
    client = MongoClient('localhost', 27017)
    db = client['twitter_db']
    collection = db['tweeps']
 
    n = len(training.index)
    ids = list(training.index) 
    random.shuffle(ids)
    again = True
    for t_id in ids: 
        if collection.find({'id': t_id}).count() > 0: 
            print "seen", t_id
        else:
            while again == True:
                try:  
                    user = api.get_user(t_id)
                    collection.insert(user)
                    print "done", t_id
                    time.sleep(5)
                    break

                except TweepError, e: 
                    #import pdb; pdb.set_trace()
                    try:
                        if e[0][0]['code'] == 88:
                            print t_id, e, "zzZZZZZz"
                            time.sleep(900)
                            continue 
                    except:
                        print str(e)
                        break

def mongo_to_CSV():
    client = MongoClient('localhost', 27017)
    db = client['twitter_db']
    collection = db['tweeps']
    with open('data/user_feats.csv', 'wt') as f:
        writer = csv.writer(f)
        writer.writerow(("id", "screen_name", "name", "verified",\
                    "description", "favourites_count", "followers_ct", \
                    "friends_ct", "tweets_ct"))
        for doc in collection.find({}, \
                    {'id':1,
                    'screen_name': 1,
                    'name': 1,
                    'verified':1,
                    'description': 1,
                    'favourites_count':1,
                    'followers_count':1,
                    'friends_count':1,
                    'tweets_count':1}):
            print doc['id']
            writer.writerow([unicode(s).encode('utf-8')\
                    for s in doc.values()])

def getUserFeatures(training, api):
    with open('data/userfeatures2.csv', 'wt') as f:
         
        writer = csv.writer(f)
        writer.writerow(("id", "screenname", "name", "verified",\
                "desc", "favorites_ct", "followers_ct", \
                "friends_ct", "tweets_ct"))
        n = len(training.index)
        ids = list(training.index) 
        random.shuffle(ids)
        again = True
        for t_id in ids: 
            
            while again == True:
                try: 
                    print t_id
                    user = api.get_user(t_id)
                    screenname = user.screen_name
                    name = user.name
                    verified = user.verified
                    description = user.description
                    favorites_ct = user.favourites_count
                    followers_ct = user.followers_count
                    friends_ct = user.friends_count
                    tweets_ct = user.statuses_count
                    writer.writerow([unicode(s).encode("utf-8") for s in (t_id, screenname, name, verified, \
                            description, favorites_ct, followers_ct, \
                            friends_ct, tweets_ct)])
                    print "done", t_id
                    time.sleep(5)
                    break

                except TweepError, e: 
                    if e[0][0]['code'] == 88:
                        print t_id, e, "zzZZZZZz"
                        time.sleep(900)
                        continue 
                    else:
                        print str(e)
                        break
                
def runFeatureExtract():
    """Outputs the feature + label CSV"""
    api = init_twitt()
    training = getTraining()
    getUserFeatures(training, api)


def runUserSave():
    """Outputs the feature + label CSV"""
    api = init_json_api()
    training = getTraining()
    saveUsers(training, api)

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

def init_linearModel(training_path='data/lr_train.csv'):
    """ linear regression baseline, on tiny feature set"""
    from sklearn.linear_model import LinearRegression
    training = pandas.DataFrame.from_csv(training_path)
    training = training.as_matrix()
    X = training[:, 0:5]
    Y = training[:,5]
    lr = LinearRegression()
    lr.fit(X,Y)
    return lr

def evaluateModel(model, test_path='data/lr_test.csv'):
    testing = pandas.DataFrame.from_csv(test_path)
    testing = testing.as_matrix()
    X_test = testing[:, 0:5]
    Y_test = testing[:,5]
    pred = model.predict(X_test)
    # for linear regression they have to binarize it
    # treats it like binary classif
    pred = pred.round()
    accuracy = sklearn.metrics.accuracy_score(Y_test, pred)
    print 'Accuracy: ', round(accuracy * 100, 2), '%'

if __name__ == '__main__':
    #runFeatureExtract()
    #runUserSave()
    mongo_to_CSV() 
