import scraper
import urllib2
import re

req = urllib2.Request("http://www.smashwords.com/extreader/read/562/5/101-degrees-fahrenheit")
con = urllib2.urlopen(req)
text = con.read()
paragraphs = re.findall(r"<P STYLE[^>]*>\n.*\n.*", text)

list = []
for par in paragraphs:
	par = re.sub("\n", "", par)
	par = re.sub("&rdquo;", "", par)
	par = re.sub("&ldquo;", "", par)
	par = re.sub("&rsquo;", "", par)
	list.append(re.sub(r"<(.|\n)*?>", "", par))
