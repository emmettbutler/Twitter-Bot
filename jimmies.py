from twitter.api import Twitter
from twitter.oauth import OAuth, read_token_file

def search_client():
    client = Twitter(domain='search.twitter.com')
    client.uriparts = ()
    return client

c = search_client()
c.Get
