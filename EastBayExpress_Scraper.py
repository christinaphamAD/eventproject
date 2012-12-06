#This script parses html from events.berkeley.edu and returns event info in JSON format
#Runs in python 2.7*

from lxml import html
from lxml import etree

source = "http://www.eastbayexpress.com/ebx/EventSearch?sortType=title&gpt=1&gpt=1&neighborhoodGroup=1094107"
origin = "EastBayExpress"
parsedObj = html.parse(source)

#Get data for database from parsedObj
names = parsedObj.xpath('//*[@class="listing"]/h3/a/text()')
ids=[]
for i in range(len(names)): ids.append(i)
##dates = parsedObj.xpath("//*[@id='content']/div/p[1]/text()")
description = parsedObj.xpath('//*[@class="listing"]/div/text()')
#coming soon: location
links = parsedObj.xpath('//*[@class="listing"]/h3/a/@href')
dates = parsedObj.xpath('//*[@class="listing"]/text()[preceding::br]')

##
#Normalize names
def normalize(someList):
    for i in someList:
        someList[someList.index(i)]=i.strip()
        try: someList.remove("")
        except:pass
    return someList

names = normalize(names)
description = normalize(description)
dates = normalize(normalize(normalize(dates)))

###normalize dates
##for i in dates:
##    x = i.replace('\t','')
##    dates[dates.index(i)] = x.replace('\n','')
##
###### Note: JSON will be replaced by CSV formatting in next update   
##eventData = []
##def formatJSON(names,dates,descriptions,origin):
##    for i in range(len(ids)):
##        eventData.append("\n['"+str(i+1)+"':['name':'"+names[i]+"','date':'"+dates[i]+"','description':'"+descriptions[i]+"']]")
##    return eventData
##
##def saveJSON(data,origin):
##    alldata = ",".join(data)
##    alldata.strip("\n")
##    f=open('events.js','w')
##    f.write(("//JSON data\nvar "+origin+" = {'Events':["+alldata+"]}").encode("utf8"))
##saveJSON(eventData,origin)
##            
##jsonData = formatJSON(names,dates,descriptions,origin)
##saveJSON(jsonData)
