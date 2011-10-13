import urllib2
import re
import random

def escapes(string):
	string = re.sub("\n", " ", string)
	string = re.sub("&rdquo;", "", string)
	string = re.sub("\x92", "", string)
	string = re.sub("&nbsp;", "", string)
	string = re.sub("Back | Next Framed", "", string)
	string = re.sub("&quot;", "", string)
	string = re.sub("&ldquo;", "", string)
	string = re.sub("&rsquo;", "", string)
	string = re.sub("&mdash;", "", string)
	string = re.sub(r"(\xa6|\x98|\xe2|\x80|\x99|\x9d|\x9c)", "", string)
	string = re.sub(r"<(.|\n)*?>", " ", string)
	return string

def random_start_word(string):
	string = string.split()
	word = random.choice(string)
	string = ' '.join(string)
	index = string.index(word)
	return string[index:]

def sci_fi():
	books = {'0671877941': 20, '067131940X': 50, '0671319760': 76, '0743499107': 6, '067187800X': 26}
	book = random.choice(books.keys())
	chapter = str(random.randint(1, books[book]))
	underscore_num = 4 - len(str(chapter))
	url = "http://www.webscription.net/10.1125/Baen/"+book+"/"+book
	for i in range(underscore_num):
		url += "_"

	url += chapter+".htm"
	req = urllib2.Request(url)
	con = urllib2.urlopen(req)
	text = con.read()
	paragraphs = re.findall(r"<P [^>]*>\n*.+\n*.+", text, flags=re.IGNORECASE)

	listing = []
	for par in paragraphs:
		listing.append(escapes(par))

	l = random.choice(listing)
	return random_start_word(l)


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
		listing.append(escapes(par))

	l = random.choice(listing)
	return random_start_word(l)


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
	part1 = ""
	part2 = ""
	upper1 = random.randint(30, 60)
	upper2 = random.randint(80, 100)
	chooser = random.randint(0, 2)
	if chooser == 0:
		part1 = urban_dict()
	elif chooser == 1:
		part1 = romance()
	else:
		part1 = sci_fi()
	chooser = random.randint(0, 2)
	if chooser == 0:
		part2 = urban_dict()
	elif chooser == 1:
		part2 = romance()
	else:
		part2 = sci_fi()
	return (part1[:upper1] + " " + part2[:upper2])[0:random.randint(120, 140)]

if __name__ == '__main__':
	print hybrid()
