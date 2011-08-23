import urllib2
from re import findall
from collections import defaultdict

def get_page(url):
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib2.urlopen(req)
    return con.read()

def parse_lines(string):
    retval = ''
    for char in string:
        retval += char if not char == '\n' else ''
        if char == '\n':
            yield retval
            retval = ''
    if retval:
        yield retval

def find_perline(line, search):
    matches = findall(search, line)
    if len(matches) is not 0:
        return len(matches)
    return 0

def count(haystack, needle):
    """
    Performs a linewise count of the occurrences of regex (needle) in string (haystack)
    Returns a defaultdict of form {'needle': occurrences}

    >>> response = get_page('http://wikipedia.com/wiki/Barack_Obama')
    >>> print count(response, "Barack Obama")['Barack Obama']
    348
    """
    d = defaultdict(int)
    lines = parse_lines(haystack)
    line = ''
    while line != '</html>':
        line = lines.next()
        d[needle] += find_perline(line, needle)
    return d
