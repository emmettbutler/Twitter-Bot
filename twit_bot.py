import twitter
from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance
from scraper import urban_dict, bash_irc, hybrid, romance, sci_fi

import os
import time
import sys
import random

#replace all racial slurs and profanity with derpy words

def search_client():
    client = Twitter(domain='search.twitter.com')
    client.uriparts = ()
    return client

def post_client():
    CONSUMER_KEY='xU9hR4NPuWSRccEpRvmf4g'
    CONSUMER_SECRET='ZRKSwWKp2eCzdTs9fl9DkOEnrgOHpetojldnZCnuo'

    oauth_filename = os.environ.get('HOME', '') + os.sep + '.twitter_oauth'
    oauth_token, oauth_token_secret = read_token_file(oauth_filename)

    return Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
            secure=True, api_version='1', domain='api.twitter.com')

def search_public_feed(searcher, last_id_replied=""):
    return searcher.search(q="e", since_id=last_id_replied)['results']

def parse_hashtags(tweet):
    hashtags = []
    words = tweet.split()
    for word in words:
        if word[0] == '#':
            hashtags.append(words[words.index(word)])
    return hashtags

def compose_tweet(incoming=None):
    response = "AA"
    hashtags = []
    if incoming is not None:
        for tweet in incoming:
            incoming_tweet = tweet['text'].replace('@space_dad', '')
            incoming_asker = tweet['from_user']
            for tag in parse_hashtags(incoming_tweet):
                hashtags.append(tag)
            last_id_replied = str(tweet['id'])

    tags = random.randint(0, 1)
    tag = ""
    print hashtags
    if tags == 0 and len(hashtags) > 0:
        tag = random.choice(hashtags)

    length = 120
    if tag:
        length = 90

    make = random.randint(0, 30)
    response = ""
    while response == "":
        if make < 10:
            response = urban_dict(length=length)
        elif make < 13:
            response = sci_fi(length=length)
        elif make < 17:
            response = bash_irc(length=length)
        elif make < 25:
            response = romance(length=length)
        else:
            response = hybrid()
    print response

    return '%s %s' % (response, tag)

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
    search = True
    DEBUG = False
    if len(sys.argv) == 2:
        DEBUG = sys.argv[1]

    while True:
        try:
            if search:
                print "searching..."
                results = search_public_feed(search_client, last_id_replied=last_id_replied)
                print "Found %s results:" % (len(results))
                tweet = compose_tweet(incoming=results)
            else:
                tweet = compose_tweet()
            print "%s\n" % (tweet)
            if not tweet.isspace() and not DEBUG:
                post(post_client, tweet)
        except TwitterError,e:
            print e
            continue
        timeslp = random.randint(2000, 10000)
        if DEBUG:
            timeslp = 3
        time.sleep(timeslp)
