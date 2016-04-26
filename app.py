#!/usr/bin/python3

##-- Michael duPont
##-- Fetch data from a "near real time" JSON data source, format to
##-- be Citygram compliant, and print the list of JSON objects
##-- 2016-04-17

#Usage: python3 app.py <service>
#Web: url/?service=<service>
#Currently supports the following services:
#  police

import sys, json, hashlib
from datetime import datetime, timedelta
from requests import get
from cgi import parse_qs

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
    
    #Child classes have the option to filter objects.
    #Filter fields should be included in requiredKeys
    def filter(self):
        '''Reutrns True if an object is to be included in the features list'''
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
        #Remove non-ascii chars for hash
        hasher.update((''.join(i for i in aString if ord(i)<128)).encode('utf-8'))
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

opdReasonFilter = json.load(open('data/opdreasons.json', 'r'))
class policereport(service):
    '''Orlando Police dispatch report feed'''
    def filter(self):
        if self.properties['reason'] in opdReasonFilter:
            return False
        return True
    def makeTitle(self):
        ret = self.properties['reason'].capitalize()
        ret += ' has been reported near ' + self.properties['address'].split(',')[0]
        time = datetime.strptime(self.properties['when'], '%Y-%m-%dT%H:%M:%S')
        ret += ' on ' + time.strftime('%m/%d at %I:%M%p')
        return ret
    def makeGeoJSON(self):
        return self.properties['location']

def getTimeStamp(minAgo, strf):
    '''Returns a strf formatted timestamp a given number of minutes prior to "now"'''
    retTime = datetime.now() - timedelta(minutes=minAgo)
    return retTime.strftime(strf)

#Associates each service with its object, required keys, and fetch URL
optionDict = {
    'police': {
        'obj': policereport,
        'reqKeys': ['address', 'location', 'when', 'reason'],
        'url': ('http://brigades.opendatanetwork.com/resource/sm4t-sjt5.json?'
                '$where=when > "{}"'.format(getTimeStamp(60, '%Y-%m-%dT%H:%M:%d')))
    }
}

def main(service):
    #If the requested service is supported
    if service in optionDict:
        featureList = []
        #Create a list of service objects from JSON data source
        try: objects = json.loads(get(optionDict[service]['url']).text.strip())
        except: return '503 Service Unavailable', {'Error':'Data Fetch Error'}
        print('Number of unfiltered items to be converted:', len(objects))
        for item in objects:
            try:
                #Create new service object init'd with original object
                serv = optionDict[service]['obj'](item)
                #If original object contains all the required keys and their values are not null
                #And the data passes the service's filter
                if serv.checkForKeys(optionDict[service]['reqKeys']) and serv.filter():
                    #If the new object updates and passes validation
                    if serv.update():
                        #Append new object to featureList
                        featureList.append(serv.export())
            except Exception as e:
                print('Item error:', e)
        print('Number of items in the feature list:', len(featureList))
        #Output/print the entire collection
        return '200 OK', {'type': 'FeatureCollection' , 'features': featureList}
    #Else output/print error
    return '400 Bad Request', {'Error':'Not a valid service'}

homepage = '''
<h1>Orlando Citygram API</h1>
<p>Hi. My job is to take data streams from the Orlando public data portal and format them to be Citygram compliant. Here is a list of service urls that are publically supported:</p>
<p>
  <a href="http://orlando-citygram-api.azurewebsites.net/?service=police">http://orlando-citygram-api.azurewebsites.net/?service=police</a>
</p>
<p>This is a project by <a href="http://codefororlando.com">Code For Orlando</a>. For any issues, contact Michael duPont at <a href="mailto:michael@mdupont.com">michael@mdupont.com</a></p>
'''

def wsgi_app(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING', ''))
    if 'service' in params and len(params['service']) == 1:
        status, resp = main(params['service'][0])
        response_headers = [('Content-type', 'text/json')]
        response_body = json.dumps(resp)
    else:
        status = '200 OK'
        response_headers = [('Content-type', 'text/html')]
        response_body = homepage
    response_headers.append(('Access-Control-Allow-Origin', '*'))
    start_response(status, response_headers)
    yield response_body.encode()

if __name__ == '__main__':
    #If run from a cli for testing
    if len(sys.argv) == 2:
        print(json.dumps(main(sys.argv[1])[1], indent=2))
    #Else start the server
    else:
        from wsgiref.simple_server import make_server
        httpd = make_server('localhost', 5555, wsgi_app)
        httpd.serve_forever()