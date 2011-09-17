from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance
from scraper import urban_dict, bash_irc, hybrid

import os
import time
import sys
import random

def search_client():
    client = Twitter(domain='search.twitter.com')
    client.uriparts = ()
    return client

def post_client():
    CONSUMER_KEY=''
    CONSUMER_SECRET=''

    oauth_filename = os.environ.get('HOME', '') + os.sep + '.twitter_oauth'
    oauth_token, oauth_token_secret = read_token_file(oauth_filename)

    return Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET), 
            secure=True, api_version='1', domain='api.twitter.com')

def search_public_feed(searcher, search_string="", last_id_replied=""):
    return searcher.search(q=search_string, since_id=last_id_replied)['results']

def compose_tweet(incoming=None):
	response = "AA"
	if incoming is not None:
		incoming_tweet = incoming['text'].replace('@space_dad', '')
		incoming_asker = incoming['from_user']
		last_id_replied = str(incoming['id'])

	make = random.randint(0, 2)
	if make is 0:
		response = urban_dict()[0:120]
	elif make is 1:
		response = bash_irc()[0:120]
	else:
		response = hybrid()

	if incoming is not None:
		msg = '@%s %s (%s)' % (incoming_asker, response, last_id_replied[-4:])
	else:
		msg = '%s' % (response)
	return msg

def post(poster, msg):
    if poster.statuses.update(status=msg):
        return True
    return False

if __name__ == '__main__':
	last_id_replied = ""
	if len(sys.argv) > 1:
		last_id_replied = sys.argv[1]

	search_client = search_client()
	post_client = post_client()
	search_string = ""

	while True:
		if search_string is not "":
			results = search_public_feed(search_client, search_string=search_string, last_id_replied=last_id_replied)
			for result in results:
				tweet = compose_tweet(incoming=result)
				print "%s\n" % (tweet)
				if not tweet.isspace():
					post(post_client, tweet)
		else:
			tweet = compose_tweet()
			print "%s\n" % (tweet)
			if not tweet.isspace():
				post(post_client, tweet)
		time.sleep(600)
