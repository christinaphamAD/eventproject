from gevent import monkey; monkey.patch_all()
import sqlite3
import datetime
from bottle import route, run, debug, template, request, validate, static_file, error
import random
import json
import urllib
import time

# Import URL Parse/Scraper
# import urllib
# import urllib2
from lxml import etree
from lxml import html

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

@route('/static/:path#.+#', name='static')
def static(path):
	return static_file(path, root='static')

@route('/')
@route('/view')
@route('/home')
def ef_list():

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets FROM Events;")
	result = c.fetchall()
	c.close()

	c2 = conn.cursor()
	c2.execute("SELECT id FROM Events;")	
	id = c2.fetchall()
	c2.close()

	output = template('make_table', rows=result, rows2=id)
	return output

@route('/add', method='GET')
@route('/add/', method='GET')
@route('/new', method='GET')
@route('/new/', method='GET')
def new_item():

	if request.GET.get('save','').strip():
		name = request.GET.get('Name', '').strip()
		desc = request.GET.get('Description', '').strip()
		cat = request.GET.get('Category', '').strip()
		url = request.GET.get('Website_URL', '').strip()
		img_url = request.GET.get('Image_URL', '').strip()
		start = str(time.mktime(time.strptime(request.GET.get('Start_Date', ''),'%m/%d/%Y %H:%M')))
		end = str(time.mktime(time.strptime(request.GET.get('End_Date', ''),'%m/%d/%Y %H:%M')))
		location = request.GET.get('Location', '').strip()
		up = 0
		down = 0
		tickets = request.GET.get('Tickets', '').strip()

		address =  location
		goog_url='http://maps.googleapis.com/maps/api/geocode/json?address='+str(address)+'&sensor=false'
		search_response = urllib.urlopen(goog_url)
		search_results = search_response.read().decode("utf8")
		jsonData = json.loads(search_results)
		results = jsonData[u'results']
		geometry = results[0][u'geometry']
		
		location2 = geometry[u'location']
		lat = location2[u'lat']
		lng = location2[u'lng']

		date = datetime.datetime.now()
		
		conn = sqlite3.connect('event_finder.db')
		c = conn.cursor()

		c.execute("INSERT INTO Events ( Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (name,desc,cat,url,img_url,start,end,location,up,down,tickets,lat,lng))
		new_id = c.lastrowid

		conn.commit()
		c.close()

		return """<p>New EventFinder Location was inserted into database with ID: %s
		<br> <a href='../'>View All</a>
		</p>
		""" % new_id

	else:
		return template('new_task.tpl')

@route('/edit/<no>', method='GET')
@validate(no=int)
def edit_item(no):

	if request.GET.get('delete','').strip():
		
		conn = sqlite3.connect('event_finder.db')
		c = conn.cursor()
		c.execute("DELETE FROM Events WHERE id = ?", (no,))
		conn.commit()

		return """<p>The item number %s was successfully deleted
		<br> <a href='../'>Back</a>
		</p>
		""" %no

	if request.GET.get('save','').strip():
		name = request.GET.get('Name', '').strip()
		desc = request.GET.get('Description', '').strip()
		cat = request.GET.get('Category', '').strip()
		url = request.GET.get('Website_URL', '').strip()
		img_url = request.GET.get('Image_URL', '').strip()
		start = str(time.mktime(time.strptime(request.GET.get('Start_Date', ''),'%m/%d/%Y %H:%M')))
		end = str(time.mktime(time.strptime(request.GET.get('End_Date', ''),'%m/%d/%Y %H:%M')))
		location = request.GET.get('Location', '').strip()
		up = request.GET.get('Up_Votes', '').strip()
		down = request.GET.get('Down_Votes', '').strip()
		tickets = request.GET.get('Tickets', '').strip()
		
		address =  location
		goog_url='http://maps.googleapis.com/maps/api/geocode/json?address='+str(address)+'&sensor=false'
		search_response = urllib.urlopen(goog_url)
		search_results = search_response.read().decode("utf8")
		jsonData = json.loads(search_results)
		results = jsonData[u'results']
		geometry = results[0][u'geometry']
		
		location2 = geometry[u'location']
		lat = location2[u'lat']
		lng = location2[u'lng']
		
		conn = sqlite3.connect('event_finder.db')
		c = conn.cursor()
		c.execute("UPDATE Events SET Name = ?, Description = ?, Category = ?, Website_URL = ?, Image_URL = ?, Start_Date = ?, End_Date = ?, Location = ?, Up_Votes = ?, Down_Votes = ?, Tickets = ?, lat = ?, lng = ? WHERE id LIKE ?", (name,desc,cat,url,img_url,start,end,location,up,down,tickets,lat,lng,no))
		conn.commit()

		return """<p>The item number %s was successfully updated
		<br> <a href='../'>Back</a>
		</p>
		""" %no

	else: 
		conn = sqlite3.connect('event_finder.db')
		c = conn.cursor()
		c.execute("SELECT Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE id LIKE ?", ((str(no)),))
		cur_data = c.fetchone()

		return template('edit_task', old = cur_data, no = no)

@route('/help')
def help():

	static_file('help.html', root='.')

@route('/json:json#[1-9]+#')
def show_json(json):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Website_URL, Image_URL, Location FROM Events WHERE id LIKE ?", (json))
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}

@route('/json/<cat>')
def show_json(cat):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE Category LIKE ?", ('%'+cat+'%',))
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}

@route('/json/s/<search>')
def show_json(search):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE Name || Description LIKE ?", ('%'+search+'%',))
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}

@route('/json/t/<search>')
def show_json(search):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE Name LIKE ?", ('%'+search+'%',))
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}
		
@route('/json/c/<cost>')
def show_json(cost):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE Tickets LIKE ?", ('%'+cost+'%',))
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}
		
@route('/<id>/up')
def plus(id):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Up_Votes FROM Events WHERE ID LIKE ?", ((id),))
	result = c.fetchall()
	
	up = result[0][1]
	
	if up == None:
		up = 0
	
	up = up+1
	
	c.execute("UPDATE Events SET Up_Votes = ? WHERE id LIKE ?", (up,(id),))
	conn.commit()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return str(up)

@route('/<id>/down')
def down(id):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Down_Votes FROM Events WHERE id LIKE ?", ((id),))
	result = c.fetchall()
	
	down = result[0][1]
	
	if down == None:
		down = 0
	
	down = down+1
	
	c.execute("UPDATE Events SET Down_Votes = ? WHERE id LIKE ?", (down,(id),))
	conn.commit()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return str(down)


@route('/json')
def show_json():

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events")
	result = c.fetchall()
	c.close()

	if not result:
		return {'Locations':'This item number does not exist!'}
	else:
		return {'Locations': result}


@error(403)
def mistake403(code):
	return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
	return 'Sorry, this page does not exist!'

	
run(host='asian-central.com', port=502, server='gevent', reloader=True, debug=True)
#run(host='localhost', port=502, reloader=True, debug=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment