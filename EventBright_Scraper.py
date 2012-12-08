from lxml import etree
import time
import sqlite3

url = "http://www.eventbrite.com/xml/event_search?app_key=NFCGVAJDWYUTNK4C4M&city=San%20Francisco&date=Future&max=100&region=CA&page=10"
source = etree.parse(url)

##csvFile = open('events.csv','a')
conn = sqlite3.connect('event_finder.db')
c = conn.cursor()

#add events to database one by one
for i in range(100):
    i+=1
    try:name = str(source.xpath('/events/event['+str(i)+']/title/text()')[0])
    except: name = ''
    try:description = str(source.xpath('/events/event['+str(i)+']/organizer/long_description/text()')[0])
    except: description= ''
    try:category = str(source.xpath('/events/event['+str(i)+']/category/text()')[0])
    except:category = ""
    try:website_URL = str(source.xpath('/events/event['+str(i)+']/url/text()')[0])
    except: website_URL = ''
    try:image_url = str(source.xpath('/events/event['+str(i)+']/logo/text()')[0])
    except:image_url = ''
    try:
        start = str(source.xpath('/events/event['+str(i)+']/start_date/text()')[0])
        start = time.strptime(start,'%Y-%m-%d %H:%M:%S')#parse time
        start = str(time.mktime(start))#convert to epoch time
    except:start = ''
    try:
        end = str(source.xpath('/events/event['+str(i)+']/end_date/text()')[0])
        end = time.strptime(end,'%Y-%m-%d %H:%M:%S')#parse time
        end = str(time.mktime(end))#convert to epoch time
    except:end = ''
    try:location = location = str(source.xpath('/events/event['+str(i)+']/venue/address/text()')[0])+", "+str(source.xpath('/events/event['+str(i)+']/venue/city/text()')[0])+", "+str(source.xpath('/events/event['+str(i)+']/venue/region/text()')[0])
    except:location = ''
    try:tickets = str(source.xpath('/events/event['+str(i)+']/tickets/ticket/price/text()')[0])
    except:tickets = ''
    try:lat = str(source.xpath('/events/event['+str(i)+']/venue/latitude/text()')[0])
    except:lat = ''
    try:lng = str(source.xpath('/events/event['+str(i)+']/venue/longitude/text()')[0])
    except:lng=''
    #send record to database
    try:c.execute("INSERT into Events (Name,Description,Category,Website_URL,Image_URL,Start_Date,End_Date,Location,Tickets,lat,lng) values ('"+name+"','"+description+"','"+category+"','"+website_URL+"','"+image_url+"','"+start+"','"+end+"','"+location+"','"+tickets+"','"+lat+"','"+lng+"')")
    except: print(str(i) +" didn't get added to the database")

# Save the changes and close database
conn.commit()
conn.close()
