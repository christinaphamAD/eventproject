from gevent import monkey; monkey.patch_all()
import sqlite3
from bottle import route, run, debug, template, request, validate, static_file, error, request, response, install, uninstall
import json

from json import dumps as json_dumps

class JSONAPIPlugin(object):
	name = 'jsonapi'
	api = 1

	def __init__(self, json_dumps=json_dumps):
		uninstall('json')
		self.json_dumps = json_dumps

	def apply(self, callback, context):
		dumps = self.json_dumps
		if not dumps: return callback
		def wrapper(*a, **ka):
			r = callback(*a, **ka)

			# Attempt to serialize, raises exception on failure
			json_response = dumps(r)

			# Set content type only if serialization succesful
			response.content_type = 'application/json'

			# Wrap in callback function for JSONP
			callback_function = request.GET.get('callback')
			if callback_function:
				json_response = ''.join([callback_function, '(', json_response, ')'])

			return json_response
		return wrapper


install(JSONAPIPlugin())

@route('/static/:path#.+#', name='static')
def static(path):
	return static_file(path, root='static')

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
		

@route('/json/l/<search>')
def show_json(search):

	conn = sqlite3.connect('event_finder.db')
	c = conn.cursor()
	c.execute("SELECT ID, Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, lat, lng FROM Events WHERE Location LIKE ?", ('%'+search+'%',))
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
		

@route('/')
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

	
run(host='asian-central.com', port=8080, server='gevent', reloader=True, debug=True)
#run(host='localhost', port=502, reloader=True, debug=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment