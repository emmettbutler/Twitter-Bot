import urllib2
import re
import random


def romance():
	books = {'55003': ['maid-for-the-billionaire', 154], '562': ['101-degrees-fahrenheit', 19], '52931': ['claimed', 96], '74690': ['kiss-on-the-bridge', 152]}
	book = random.choice(books.keys())
	page = str(random.randint(2, books[book][1]))
	url = "http://www.smashwords.com/extreader/read/"+book+"/"+page+"/"+books[book][0]
	req = urllib2.Request(url)
	con = urllib2.urlopen(req)
	text = con.read()
	paragraphs = re.findall(r"<P [^>]*>\n*.+\n*.+", text, flags=re.IGNORECASE)

	listing = []
	for par in paragraphs:
		par = re.sub("\n", " ", par)
		par = re.sub("&rdquo;", "", par)
		par = re.sub("&quot;", "", par)
		par = re.sub("&ldquo;", "", par)
		par = re.sub("&rsquo;", "", par)
		par = re.sub("&mdash;", "", par)
		par = re.sub(r"(\xa6|\x98|\xe2|\x80|\x99|\x9d|\x9c)", "", par)
		listing.append(re.sub(r"<(.|\n)*?>", " ", par))

	l = random.choice(listing)
	l = l.split()
	word = random.choice(l)
	l = ' '.join(l)
	index = l.index(word)
	return l[index:]
	

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
	return (urban_dict()[:upper1] + " " + romance()[:upper2])[0:random.randint(120, 140)]

if __name__ == '__main__':
	print hybrid()
