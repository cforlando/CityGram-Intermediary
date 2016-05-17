#!/usr/bin/python3
#
#-- Michael duPont
#-- Fetch data from a "near real time" JSON data source, format to
#-- be Citygram compliant, and print the list of JSON objects
#-- 2016-04-17
#
# Usage: python3 app.py <service>
# Web: url/?service=<service>
# Currently supports the following services:
#   police

import sys, json
from requests import get
from cgi import parse_qs

from services.service_factory import ServiceFactory


def main(service):
    # Create the Service object from the factory
    serv = ServiceFactory.get_service(service)

    if serv:
        # If the requested service is supported
        featureList = []

        try:
            # Create a list of service objects from JSON data source
            objects = json.loads(get(serv.get_url()).text.strip())
        except:
            return '503 Service Unavailable', {'Error': 'Data Fetch Error'}

        print('Number of unfiltered items to be converted:', len(objects))
        for item in objects:
            try:
                # Pass the original object to the service
                processed_obj = serv.process_object(item)
                if processed_obj:
                    # Append new object to featureList
                    featureList.append(processed_obj)

            except Exception as e:
                print('Item error:', e)

        print('Number of items in the feature list:', len(featureList))
        # Output/print the entire collection
        return '200 OK', {'type': 'FeatureCollection' , 'features': featureList}
    # Else output/print error
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
    # If run from a cli for testing
    if len(sys.argv) == 2:
        print(json.dumps(main(sys.argv[1])[1], indent=2))
    # Else start the server
    else:
        from wsgiref.simple_server import make_server
        httpd = make_server('localhost', 5555, wsgi_app)
        httpd.serve_forever()
