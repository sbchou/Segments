import csv
import twitter

CONSUMER_KEY = 'FoM0fWB74mAbDtOMoZYZpDfY5'
CONSUMER_SECRET = 'ErOuMyvNORMBYufZrJYYcJal4IdtAWlnncQsVtTDaxY16mV0Xi'
ACCESS_KEY = '359150678-ifOaGTIxHl6lB99GBOQVt3VAG4h3fB5vUxph6l1O'
ACCESS_SECRET = '3lgZ1YtZcAKMpyQ9pv5oCWda534yxPBlf92RmfuRPdo0E'

api = twitter.Api(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token_key = ACCESS_KEY, access_token_secret = ACCESS_SECRET)

user_ids = ['359150678', '813286']
users = api.UsersLookup(user_id=user_ids)

c = csv.writer(open("user_features.csv", "wb"))
c.writerow(["id", "username", "name",])

for t in users:
    c.writerow([t.GetId(), t.GetScreenName(), t.GetName()])

