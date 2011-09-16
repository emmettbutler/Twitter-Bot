import urllib2
import re
import random


def urban_dict():
    req = urllib2.Request("http://www.urbandictionary.com/random.php", headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    text = con.read()
    matches = re.search(r"<div class..definition\b[^>]*>(.+?)</div>", text)
    definition = re.sub(r"<(.|\n)*?>", "", matches.group(0))
    definition = definition.replace("Urban Dictionary", "")
    definition = definition.replace("&quot;", "")
    d = definition.split()
    word = random.choice(d)
    d = ' '.join(d)
    index = d.index(word)
    return d[index:]

def bash_irc():
    req = urllib2.Request("http://bash.org/?random", headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    text = con.read()
    matches = re.search(r"<p class..qt\b[^>]*>(.+?)</p>", text)
    quote = re.sub(r"<(.|\n)*?>", "", matches.group(0))
    quote = re.sub(r"(&.*;|\"|\'|&nbsp|\(.*\)|\[.*\]|&quot;.*&quot;|&lt;.*&gt;)", "", quote)
    q = quote.split()
    if q:
        w = random.choice(q)
        q = ' '.join(q)
        index = q.index(w)
        return q[index:]
    else:
        return urban_dict()

def hybrid():
	upper1 = random.randint(30, 60)
	upper2 = random.randint(80, 100)
	return (urban_dict()[:upper1] + bash_irc()[:upper2])[0:random.randint(120, 140)]

if __name__ == '__main__':
	print hybrid()
