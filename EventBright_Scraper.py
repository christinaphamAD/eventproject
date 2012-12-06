from lxml import etree
from lxml import html
import json
import urllib

url = "https://www.eventbrite.com/xml/event_search?app_key=NFCGVAJDWYUTNK4C4M&city=Berkeley&date=Future&max=100"
source = url.parse(url)

print source

##search_response = urllib.urlopen(url)
##search_results = search_response.read().decode("utf8")
##results = json.loads(search_results)
##print results
##p = etree.parse(url)
##print p
