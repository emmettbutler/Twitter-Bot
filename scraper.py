import urllib2
import re
import random

headers = {'User-Agent': "Magic Browser"}


def escapes(string):
    string = re.sub(r"<(.|\n)*?>", " ", string)
    string = re.sub("(Urban Dictionary|Framed|Back|Next)", "", string)
    string = re.sub(r"(\xa6|\x98|\xe2|\x80|\x99|\x9d|\x9c|\x92|\&.*;)", "", string)
    return string


def random_word_range(string, length):
    string = string.split()
    punc_index = 0
    for word in string:
        if '.' in word:
            punc_index = string.index(word)
            break
    top = random.randint(0, len(string) / 2)
    if punc_index:
        bottom = punc_index
    else:
        if len(string) > 1:
            bottom = random.randint((len(string) / 2) + 1, len(string))
        else:
            bottom = 1
    counter = 0
    while len(' '.join(string[top:bottom])) > length:
        top = random.randint(0, len(string) / 2)
        bottom = random.randint((len(string) / 2) + 1, len(string) - counter)
        if counter > (len(string) / 2) + 2:
            counter -= 1
    return ' '.join(string[top:bottom])


def sci_fi(length=120):
    #the unique url segment corresponding to a book and the number of
    #chapters it has
    books = {
        '0671877941': 20,
        '067131940X': 50,
        '0671319760': 76,
        '0743499107': 6,
        '067187800X': 26
    }
    book = random.choice(books.keys())

    #choose a random chapter from within the range defined by books[book]
    chapter = str(random.randint(1, books[book]))

    #build the url, starting with the first part
    url = "http://www.webscription.net/10.1125/Baen/" + book + "/" + book
    #include the proper number of underscores based on the number of digits
    #in the chapter number
    for i in range(4 - len(str(chapter))):
        url += "_"
    url += chapter + ".htm"

    req = urllib2.Request(url, headers=headers)
    con = urllib2.urlopen(req)
    text = con.read()

    #find the paragraphs of usable text with a regex
    paragraphs = re.findall(r"<P [^>]*>\n*.+\n*.+", text, flags=re.IGNORECASE)

    listing = []
    #build a list of escaped paragraphs
    for par in paragraphs:
        listing.append(escapes(par))

    l = random.choice(listing)
    return random_word_range(l, length)


def romance(length=120):
    #list of book ids, titles, and corresponding number of pages
    #both book id and title are needed to build the urls
    books = {
        '85389': ['heaven-can-wait', 346],
        '46442': ['convenient-love', 22],
        '75112': ['letter-of-love', 40],
        '55003': ['maid-for-the-billionaire', 154],
        '562': ['101-degrees-fahrenheit', 19],
        '52931': ['claimed', 96],
        '74690': ['kiss-on-the-bridge', 152]
    }
    book = random.choice(books.keys())
    page = str(random.randint(2, books[book][1]))

    url = "http://www.smashwords.com/extreader/read/" + book + "/" + page + "/" + books[book][0]
    req = urllib2.Request(url, headers=headers)
    con = urllib2.urlopen(req)
    text = con.read()

    paragraphs = re.findall(r"<P [^>]*>\n*.+\n*.+", text, flags=re.IGNORECASE)

    listing = []
    for par in paragraphs:
        listing.append(escapes(par))

    l = random.choice(listing)
    return random_word_range(l, length)


def urban_dict(length=120):
    req = urllib2.Request(
        "http://www.urbandictionary.com/random.php",
        headers=headers
    )

    con = urllib2.urlopen(req)
    text = con.read()

    matches = re.search(r"<div class..definition\b[^>]*>(.+?)</div>", text)
    definition = escapes(matches.group(0))
    return random_word_range(definition, length)


def bash_irc(length=120):
    req = urllib2.Request(
        "http://bash.org/?random",
        headers=headers
    )

    con = urllib2.urlopen(req)
    text = con.read()

    matches = re.search(r"<p class..qt\b[^>]*>(.+?)</p>", text)

    if matches.group(0):
        quote = escapes(matches.group(0))
        quote = re.sub(
            r"(&.*;|\"|\'|&nbsp|\(.*\)|\[.*\]|&quot;.*&quot;|&lt;.*&gt;)",
            "",
            quote
        )
        return random_word_range(quote, length)
    else:
        return urban_dict()


def hybrid():
    upper1, upper2 = (random.randint(1, 80) for a in range(0, 2))

    chooser = random.randint(0, 3)
    part1 = random_site_scrape(chooser, 60)

    chooser = random.randint(0, 3)
    part2 = random_site_scrape(chooser, 60)

    return (part1[:upper1] + " " + part2[:upper2])


def random_site_scrape(chooser, length):
    if chooser == 0:
        return urban_dict(length=length)
    elif chooser == 1:
        return romance(length=length)
    elif chooser == 2:
        return bash_irc(length=length)
    else:
        return sci_fi(length=length)

if __name__ == '__main__':
    print hybrid()
