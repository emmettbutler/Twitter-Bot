from twitter.api import Twitter
from twitter.oauth import OAuth, read_token_file
from scraper import urban_dict, bash_irc, hybrid, romance, sci_fi
from mygengo import MyGengo

import os
import time
import sys
import random

import secret

#replace all racial slurs and profanity with derpy words

def search_client():
    client = Twitter(domain='search.twitter.com')
    client.uriparts = ()
    return client


def post_client():

    oauth_filename = os.environ.get('HOME', '') + os.sep + '.twitter_oauth'
    oauth_token, oauth_token_secret = read_token_file(oauth_filename)

    return Twitter(
        auth=OAuth(
            oauth_token,
            oauth_token_secret,
            secret.TWITTER_CONSUMER_KEY,
            secret.TWITTER_CONSUMER_SECRET
        ),
        secure=True,
        api_version='1',
        domain='api.twitter.com'
    )


def search_public_feed(searcher, last_id_replied=""):
    return searcher.search(q="e")['results']


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
    tags = random.randint(0, 3)
    tag = ""

    if incoming is not None and tags == 0:
        print "Searching for hashtags..." if DEBUG else ''
        for tweet in incoming:
            incoming_tweet = tweet['text'].replace('@space_dad', '')
            for tag in parse_hashtags(incoming_tweet):
                hashtags.append(tag)

    if tags == 0 and len(hashtags) > 0:
        print hashtags if DEBUG else ''
        tag = random.choice(hashtags)
        print "Chose hashtag: %s" % tag if DEBUG else ''

    length = 120
    if tag:
        length = 90

    make = random.randint(0, 30)
    response = ""
    while response == "":
        print "Selecting source..." if DEBUG else ''
        if make < 10:
            print "Chose Urban Dictionary\nSearching..." if DEBUG else ''
            response = urban_dict(length=length)
            print response if DEBUG else ''
        elif make < 13:
            print "Chose science fiction\nSearching..." if DEBUG else ''
            response = sci_fi(length=length)
            print response if DEBUG else ''
        elif make < 17:
            print "Chose bash.org\nSearching..." if DEBUG else ''
            response = bash_irc(length=length)
            print response if DEBUG else ''
        elif make < 25:
            print "Chose romance books\nSearching..." if DEBUG else ''
            response = romance(length=length)
            print response if DEBUG else ''
        else:
            print "Chose hybrid\nSearching..." if DEBUG else ''
            response = hybrid()
            print response if DEBUG else ''

    if random.randint(0, 1) == 1:
        print "Translating tweet..." if DEBUG else ''
        response = translate(response)
        print "%s" % response if DEBUG else ''

    #disable hashtags
    tag = ""
    return '%s %s' % (response, tag)


def post(poster, msg):
    if poster.statuses.update(status=msg):
        return True
    return False


def translate(text):
    gengo = MyGengo(
        public_key=secret.GENGO_PUBLIC_KEY,
        private_key=secret.GENGO_PRIVATE_KEY,
        sandbox=False
    )
    counter = 0
    to_lang = 'en'
    from_lang = 'ja'
    while counter < 4:  # even number = English result
        translation = gengo.postTranslationJob(job={
            'type': 'text',
            'slug': 'the_game',
            'body_src': text,
            'lc_src': to_lang,
            'lc_tgt': from_lang,
            'tier': 'machine'
        })
        text = translation['response']['job']['body_tgt']
        swap = to_lang
        to_lang = from_lang
        from_lang = swap
        counter += 1
    return text

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
                results = search_public_feed(
                                search_client,
                                last_id_replied=last_id_replied
                            )
                tweet = compose_tweet(incoming=results)
            else:
                tweet = compose_tweet()
            print "Final tweet: '%s'" % tweet
            if not tweet.isspace() and not DEBUG:
                post(post_client, tweet)
        except:
            continue
        timeslp = 3 if DEBUG else 1200
        print "\n\n" if DEBUG else ''
        time.sleep(timeslp)
