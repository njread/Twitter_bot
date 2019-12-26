from datetime import datetime
import tweepy
from tweepy import OAuthHandler
from os import environ
import time
from random import randrange

d = datetime.today()

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
username = environ['username']
password = environ['password']
INTERVAL = 60 * 60 * 24
# twitter api authentication 
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
# git hub username and password
g = Github(username, password)

# while loop that runs indefinitely that check if my dates.
while True:
	days_updated= []
	count = 0
	didnt_push = ["No he didnt he should feel bad!! ",
				  'No he messed up and forgot!!',
				  'Bro come on no pushes??',
				  'He is trying his best but he got tied up so no pushes today'
				  ]
	for repo in g.get_user().get_repos():
		days_updated.append(repo.updated_at.date())
	try:
		if d.date() in days_updated:
			api.update_status(f'yes he did, he updated: {repo.name} he is on a {count} day streak')
			print('I tweeted that he pushed')	
		else:
			api.update_status(f'{didnt_push[randrange(3)]} he has broke a {count} day streak')
			print('I tweeted that he did not push')
		time.sleep(INTERVAL)
		count +=1
	except:
		print('error duplicated tweet, deployed back up tweet.')
		time.sleep(INTERVAL)
		api.update_status(f'{didnt_push[randrange(3)]} he probably got on error on line {randrange(1000)} and got stuck')
		count +=1
		pass











