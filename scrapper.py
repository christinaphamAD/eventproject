#This script parses html or xml and returns event info in JSON format
from lxml import html
from lxml import etree

dates = parsedObj.xpath('//item/title/text()')
names = []
counter = 0

source = "http://events.berkeley.edu/index.php?view=summary&timeframe=month&date=2012-12-03&tab=all_events"
origin = "UC_Berkeley"
parsedObj = html.parse(source)

names = parsedObj.xpath('//div/h3/a/text()')
for i in range(len(names)):
    list1[i]=list1[i].strip()
    try:names.remove("")
    except:pass
description = parsedObj.xpath("//*[@id='content']/div/p[3]/text()")

dates = parsedObj.xpath("//*[@id='content']/div/p[1]/text()")

#normalize dates
for i in dates:
    x = i.replace('\t','')
    dates[dates.index(i)] = x.replace('\n','')


print(dates)
print(names)

descriptions = parsedObj.xpath("//item/description/text()")
print (descriptions)

##links = parsedObj.xpath("//item/link/")
ids=[]
for i in range(len(names)): ids.append(i)
    
eventData = []
def formatJSON(names,dates,descriptions,origin):
    for i in range(len(ids)):
        eventData.append("\n['"+str(i+1)+"':['name':'"+names[i]+"','date':'"+dates[i]+"','description':'"+descriptions[i]+"']]")
    return eventData

def saveJSON(data,origin):
    alldata = ",".join(data)
    alldata.strip("\n")
    f=open('events.js','w')
    f.write(("//JSON data\nvar "+origin+" = {'Events':["+alldata+"]}").encode("utf8"))
saveJSON(eventData,origin)
            
jsonData = formatJSON(names,dates,descriptions,origin)
saveJSON(jsonData)
