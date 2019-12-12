from github import Github
from datetime import datetime
import tweepy
from tweepy import OAuthHandler

# First create a Github instance:
d = datetime.today()
ckey = CONSUMER_KEY
csecret = CONSUMER_SECRET
atoken = ACCESS_KEY
asecret = ACCESS_SECRET
INTERVAL = 60 * 60 * 6

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


# using username and password
g = Github(keys.username, keys.password)
days_updated= []
# Then play with your Github objects:
for repo in g.get_user().get_repos():
    if d.date() == repo.updated_at.date():
        api.update_status(f'yes he did, he updated: {repo.name}')
