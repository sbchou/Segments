import csv
import twitter
import pandas
from sklearn import svm

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'

api = twitter.Api(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token_key = ACCESS_KEY, access_token_secret = ACCESS_SECRET)
 
def get_twitter_features():
    c = csv.writer(open("user_features.csv", "wb"))
    c.writerow(["id", "username", "name",])

    # -1 for M, 1 for F
    labeled = pandas.DataFrame.from_csv('labels.csv')
    ids = [str(i) for i in labeled.index]

    # do it in chunks of 100 because overload api
    for i in xrange(0, len(ids), 100):
        j = i + 100 if i + 100 <= len(ids) else len(ids)
        users = api.UsersLookup(user_id=ids[i:j]) 
        for t in users:
            # IF USER IS IN ENG
            c.writerow([t.GetId(),\
                        t.GetScreenName().encode('ascii', 'ignore'),\
                        t.GetName().encode('ascii', 'ignore')])
            
def gender_baseline():
    model = svm.SVC(probability=True)
    X = 









