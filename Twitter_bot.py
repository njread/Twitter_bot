from github import Github
from datetime import datetime
import tweepy
from tweepy import OAuthHandler
from os import environ
import time

d = datetime.today()

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
username = environ['username']
password = environ['password']
INTERVAL = 60 * 60 * 24

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# using username and password
g = Github(username, password)
days_updated= []
count = 0
# while loop that runs indefinitely that check if my dates.
while True:
	for repo in g.get_user().get_repos():
		days_updated.append(repo.updated_at.date())
	if d.date() in repo.updated_at.date():
		api.update_status(f'yes he did, he updated: {repo.name}')
		count +=1
	else:
		api.update_status(f"No he didn't he broke a {count} day long streak")
	time.sleep(INTERVAL)
