##-- Michael duPont
##-- Fetch data from a "near real time" JSON data source, format to
##-- be Citygram compliant, and print the list of JSON objects
##-- 2016-04-17

import json
from datetime import datetime
from services.service import Service


class PoliceReport(Service):
    '''
    Orlando Police dispatch report feed
    Child class definitions must implement makeTitle() and makeGeoJSON()
    '''

    tag = "police"  # Service identifier (tag)

    def __init__(self):
        super().__init__()
        self.opdReasonFilter = json.load(open('data/opdreasons.json', 'r'))
        self.reqKeys = ['address', 'location', 'when', 'reason']
        self.url = 'http://brigades.opendatanetwork.com/resource/sm4t-sjt5.json?'
        self.time_window = 720  # Number of minutes for the timerame

    def get_url(self):
        # Not sure if this logic is just for PoliceReport or all services.
        return self.url + ('$where=when > "{}"'.format(Service.get_timestamp(self.time_window,
                                                                             '%Y-%m-%dT%H:%M:%d')))

    def filter(self):
        if self.properties['reason'] in self.opdReasonFilter:
            return False
        return True

    def _make_title(self):
        ret = self.properties['reason'].capitalize()
        ret += ' has been reported near ' + self.properties['address'].split(',')[0]
        time = datetime.strptime(self.properties['when'], '%Y-%m-%dT%H:%M:%S')
        times = [time.strftime(i).lstrip('0') for i in ('%m', '%d', '%I:%M%p')]
        ret += ' on {}/{} at {}'.format(times[0], times[1], times[2])
        return ret

    def _make_geo_json(self):
        return self.properties['location']