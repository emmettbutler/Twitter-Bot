import serial
import storm_secret as secret
import os
import sys
import time
from twitter.api import Twitter
from twitter.oauth import OAuth, read_token_file

def search_client():
    client = Twitter(domain='search.twitter.com')
    client.uriparts = ()
    return client

def search_public_feed(searcher, query="bees", last_id_replied=""):
    return searcher.search(q=query)['results']

if __name__ == '__main__':
    q = "bees"
    if len(sys.argv) > 1:
        q = sys.argv[1]

    search_client = search_client()

    ser = serial.Serial("/dev/tty.usbserial-A800eHXH", 9600)
    cache = []

    while True:
        print "Searching public feed"
        results = search_public_feed(search_client, query=q)
        for tweet in results:
            if tweet not in cache:
                cache.append(tweet)
                sig = tweet['text'].encode('ascii', 'ignore')
                print "Sending tweet '%s' over serial connection" % (sig)
                #sig = "".join(sorted(sig))
                ser.write("%s\0" % (sig))
        print "Sleeping..."
        time.sleep(2)

    ser.close()
