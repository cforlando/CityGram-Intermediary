#!/usr/bin/python3

##-- Michael duPont
##-- interHandler.py
##-- Fetch data from a "near real time" JSON data source, format to
##-- be Citygram compliant, and print the list of JSON objects
##-- 2016-02-02

#Usage: python interHandler.py <service>
#Currently supports the following services:
#  - police

import sys, json, hashlib
from datetime import datetime, timedelta
from requests import get

def output(aDict):
	'''Prints a formatted JSON string of 'aDict' and exits the script'''
	print(json.dumps(aDict))
	sys.exit()

#Send error message if not correct number of options
if len(sys.argv) != 2: output({'Error':'Bad input'})

def getJSON(url):
	'''Returns a dict (from JSON) from a given URL'''
	try:
		return json.loads(get(url).text.strip())
	except:
		output({'Error':'Data Fetch Error'})

class service:
	'''Service parent class definition'''
	id = ''
	geojson = {}
	
	def __init__(self , propList):
		'''Class init where propList is the original object library'''
		self.properties = propList
	
	def checkForKeys(self , keyList):
		'''Returns True if all given keys are in properties'''
		for item in keyList:
			if item not in self.properties: return False
			elif self.properties[item] in ['','NULL']: return False
		return True
	
	#The next two require child-specific implementation
	def makeTitle(self):
		'''Returns a string fully describing the alert/event'''
		return ''
	
	def makeGeoJSON(self):
		'''Returns a Citygram-compliant geometry dictionary'''
		return {}
	
	def setID(self , aString):
		'''Set the object id to be equal to the SHA-1 hex value of a string'''
		hasher = hashlib.sha1()
		#Remove non-ascii chars
		hasher.update(''.join(i for i in aString if ord(i)<128))
		self.id = hasher.hexdigest()
	
	def validate(self):
		'''Returns True if object passes all validation tests'''
		try:
			assert('title' in self.properties)  #A title has been set in the properties dict
			assert(type(self.id) == str)        #The id is a string
			assert(self.id != '')               #The id has been changed
			assert(type(self.geojson) == dict)  #The geoLoc is a dict
			assert(self.geojson != {})          #The geoLoc has been changed
			return True
		except: return False
	
	def update(self):
		'''Formats and sets required data fields and runs verification
		test. Returns True if successful, else False'''
		try:
			title = self.makeTitle()
			self.properties['title'] = title
			self.setID(title)
			self.geojson = self.makeGeoJSON()
			return self.validate()
		except:
			return False
	
	def export(self):
		'''Returns a Citygram-compliant version of the original object'''
		return {
			'id': self.id,
			'type': 'Feature',
			'geometry': self.geojson,
			'properties': self.properties
		}

##--Child class definitions must implement makeTitle() and makeGeoJSON()

class policereport(service):
	'''Orlando Police dispatch report feed'''
	
	def makeTitle(self):
		ret = self.properties['reason'].capitalize()
		ret += ' has occured at ' + self.properties['location']
		ret += ' at ' + self.properties['when']
		return ret
	def makeGeoJSON(self):
		return {
			'type': 'point',
			'coordinates': {
				'latitude': self.properties['location']['coordinates'][0],
				'longitude': self.properties['location_1']['longitude']
			}
		}

def getTimeStamp(minAgo, strf):
	'''Returns a strf formatted timestamp a given number of minutes prior to "now"'''
	retTime =  datetime.now() - timedelta(minutes=minAgo)
	return retTime.strftime(strf)

#Associates each service with its object, required keys, and fetch URL
optionDict = {
	'police': {
		'obj': policereport,
		'reqKeys': ['address', 'location', 'when', 'reason'],
		'url': ('http://brigades.opendatanetwork.com/resource/sm4t-sjt5.json?'
				'$where=when > "{}"'.format(getTimeStamp(15, '%Y-%m-%dT%H:%M:%d')))
	}
}

#MAIN SCRIPT
request = sys.argv[1]
#If the requested service is supported
if request in optionDict:
	featureList = []
	#Create a list of service objects from JSON data source
	objects = getJSON(optionDict[request]['url'])
	for item in objects:
		#Create new service object init'd with original object
		serv = optionDict[request]['obj'](item)
		#If original object contains all the required keys and their values are not null
		if serv.checkForKeys(optionDict[request]['reqKeys']):
			#If the new object updates and passes validation
			if serv.update():
				#Append new object to featureList
				featureList.append(serv.export())
	#Output/print the entire collection
	output({'type': 'FeatureCollection' , 'features': featureList})
#Else output/print error
else: output({'Error':'Not a valid service'})
