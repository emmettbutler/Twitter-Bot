import urllib2
import re

def request_definition():
    req = urllib2.Request("http://www.urbandictionary.com/random.php", headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    text = con.read()
    matches = re.search(r"<div class..definition\b[^>]*>(.+?)</div>", text)
    definition = re.sub(r"<(.|\n)*?>", "", matches.group(0))
    definition = definition.replace("Urban Dictionary", "")
    definition = definition.replace("&quot;", "")
    return definition

if __name__ == '__main__':
	print request_definition()[20:120]
