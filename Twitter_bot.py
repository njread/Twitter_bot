from github import Github
from datetime import datetime
import tweepy
import time
from tweepy import OAuthHandler
import keys
from os import environ
# First create a Github instance:
d = datetime.today()
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
INTERVAL = 60 * 60 * 12

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


# using username and password
g = Github(username, password)
days_updated= []
# Then play with your Github objects:
while True:
	for repo in g.get_user().get_repos():
		if d.date() == repo.updated_at.date():
			api.update_status(f'yes he did, he updated: {repo.name}')
	time.sleep(INTERVAL)
