
from HTMLParser import HTMLParser
from urllib2 import urlopen

class Spider(HTMLParser):
    def __init__(self,url):
        HTMLParser.__init__(self)
        req=urlopen(url)
        self.feed(req.read())

    def handle_starttag(self,tag,attrs):
        if tag=='p'and attrs:
            for i in attrs:
                print "%s %s\n" % i

Spider('http://www.webscription.net/10.1125/Baen/0671578456/0671578456___1.htm')
