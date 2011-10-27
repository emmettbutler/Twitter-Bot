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

def random_word_range(string, length):
    string = string.split()
    punc_index = 0
    for word in string:
        if '.' in word:
            punc_index = string.index(word)
            break
    top = random.randint(0, len(string)/2)
    if punc_index:
        bottom = punc_index
    else:
        bottom = random.randint((len(string)/2)+1, len(string))
    counter = 0
    while len(' '.join(string[top:bottom])) > length:
        top = random.randint(0, len(string)/2)
        bottom = random.randint((len(string)/2)+1, len(string)-counter)
        if counter > (len(string)/2)+2:
            counter -= 1
    return ' '.join(string[top:bottom])

    """
    word = random.choice(string)
    string = ' '.join(string)
    index = string.index(word)
    return string[index:]
    """

def sci_fi(short=False):
    length = 120
    if short:
        length = 60

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
    return random_word_range(l, length)


def romance(short=False):
    length = 120
    if short:
        length = 60

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
    return random_word_range(l, length)


def urban_dict(short=False):
    length = 120
    if short:
        length = 60

    req = urllib2.Request("http://www.urbandictionary.com/random.php", headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    text = con.read()
    matches = re.search(r"<div class..definition\b[^>]*>(.+?)</div>", text)
    definition = re.sub(r"<(.|\n)*?>", "", matches.group(0))
    definition = definition.replace("Urban Dictionary", "")
    definition = definition.replace("&quot;", "")
    return random_word_range(definition, length)

def bash_irc(short=False):
    length = 120
    if short:
        length = 60

    req = urllib2.Request("http://bash.org/?random", headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    text = con.read()
    matches = re.search(r"<p class..qt\b[^>]*>(.+?)</p>", text)
    quote = re.sub(r"<(.|\n)*?>", "", matches.group(0))
    quote = re.sub(r"(&.*;|\"|\'|&nbsp|\(.*\)|\[.*\]|&quot;.*&quot;|&lt;.*&gt;)", "", quote)
    if quote:
        return random_word_range(quote, length)
    else:
        return urban_dict()

def hybrid():
    part1 = ""
    part2 = ""
    upper1 = random.randint(1, 80)
    upper2 = random.randint(1, 80)
    chooser = random.randint(0, 3)
    if chooser == 0:
        part1 = urban_dict(True)
    elif chooser == 1:
        part1 = romance(True)
    elif chooser == 2:
        part2 = bash_irc(True)
    else:
        part1 = sci_fi()
    chooser = random.randint(0, 3)
    if chooser == 0:
        part2 = urban_dict(True)
    elif chooser == 1:
        part2 = romance(True)
    elif chooser == 2:
        part2 = bash_irc(True)
    else:
        part2 = sci_fi(True)
    return (part1[:upper1] + " " + part2[:upper2])

if __name__ == '__main__':
    print hybrid()
