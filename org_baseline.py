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
import sys

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

def mongo_to_CSV(OUT_PATH):
    client = MongoClient('localhost', 27017)
    db = client['twitter_db']
    collection = db['tweeps']
    with open(OUT_PATH, 'wt') as f:
        writer = csv.writer(f)
        writer.writerow(("id", "screen_name", "name", "verified",\
                    "description", "favourites_count", "followers_count", \
                    "friends_count", "statuses_count"))
        for doc in collection.find({}, \
                    {'id':1,
                    'screen_name': 1,
                    'name': 1,
                    'verified':1,
                    'description': 1,
                    'favourites_count':1,
                    'followers_count':1,
                    'friends_count':1,
                    'statuses_count':1}):
            print doc['id'] 
            writer.writerow([unicode(doc['id']).encode('utf-8'),\
                unicode(doc['screen_name']).encode('utf-8'),\
                unicode(doc['name']).encode('utf-8'),\
                unicode(doc['verified']).encode('utf-8'),\
                unicode(doc['description']).encode('utf-8'),\
                unicode(doc['favourites_count']).encode('utf-8'),\
                unicode(doc['followers_count']).encode('utf-8'),\
                unicode(doc['friends_count']).encode('utf-8'),\
                unicode(doc['statuses_count']).encode('utf-8')])

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

def genTraining(ratio, label_path, feature_path, out_name):
    labels = pandas.DataFrame.from_csv(label_path, sep="\t")
    features = pandas.DataFrame.from_csv(feature_path)
    joined = features.join(labels)
    joined = joined[np.isfinite(joined['type'])]
    joined['verified'] = joined['verified'] * 1 # binarize
    #split and save as train, test (4/5, 1/5)
    n = len(joined)

    subset = joined[['verified', 'favourites_count', 'followers_count', 'friends_count',\
            'statuses_count','type']]
    subset[:int(n * ratio)].to_csv(out_name + '_train.csv')
    subset[int(n * ratio):].to_csv(out_name + '_test.csv')
     
 
def init_linearModel(training_path):
    """ linear regression baseline, on tiny feature set"""
    from sklearn.linear_model import LinearRegression
    training = pandas.DataFrame.from_csv(training_path)
    training = training.as_matrix()
    X = training[:, 0:5]
    Y = training[:,5]
    lr = LinearRegression()
    lr.fit(X,Y)
    return lr

def evaluateModel(model, test_path):
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
    if sys.argv[1] == 'stream':
        runUserSave()
    if sys.argv[1] == 'csv':
        mongo_to_CSV('data/user_feats.csv')
    if sys.argv[1] == 'data':
        genTraining(0.5, \
            'data/humanizr_data/humanizr_labeled.tsv', \
            'data/user_feats.csv', \
            'data/linear')
    if sys.argv[1] == 'linear':
        lr = init_linearModel('data/linear_train.csv')
        evaluateModel(lr, 'data/linear_test.csv' )




