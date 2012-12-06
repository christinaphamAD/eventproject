import sqlite3
import json
import urllib

conn = sqlite3.connect('event_finder.db')
c = conn.cursor()
c.execute('select Location, ID from Events')
results = c.fetchall()

for row in results:
    address =  row[0]
    ID = row[1]
    url='http://maps.googleapis.com/maps/api/geocode/json?address='+str(address)+'&sensor=false'
    search_response = urllib.urlopen(url)
    search_results = search_response.read().decode("utf8")
    jsonData = json.loads(search_results)
    results = jsonData[u'results']
    geometry = results[0][u'geometry']
    location = geometry[u'location']
    lat = location[u'lat']
    lng = location[u'lng']
    c.execute("UPDATE Events SET lat=?, lng=? WHERE ID=?", (lat,lng,(ID)))


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
