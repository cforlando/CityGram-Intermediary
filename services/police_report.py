# -- Michael duPont
# -- Fetch data from a "near real time" JSON data source, format to
# -- be Citygram compliant, and print the list of JSON objects
# -- 2016-04-17

import json
from datetime import datetime
from services.service import Service


class PoliceReport(Service):
    """ Orlando Police dispatch report feed
    Child class definitions must implement makeTitle() and makeGeoJSON()
    """

    # Static Service Members
    tag = "police"  # Service identifier (tag)
    url = 'http://brigades.opendatanetwork.com/resource/sm4t-sjt5.json?'
    req_keys = ['address', 'location', 'when', 'reason']

    # Static Police Report Members
    reason_filter = json.load(open('data/opdreasons.json', 'r'))

    def _filter(self):
        """ Filters based on 'reason' field.
        :return: bool
        """
        if self.properties['reason'] in PoliceReport.reason_filter:
            return False
        return True

    def _make_title(self):
        """Returns a string fully describing the alert/event"""
        ret = self.properties['reason'].capitalize()
        ret += ' has been reported near ' + self.properties['address'].split(',')[0]
        time = datetime.strptime(self.properties['when'], '%Y-%m-%dT%H:%M:%S')
        times = [time.strftime(i).lstrip('0') for i in ('%m', '%d', '%I:%M%p')]
        ret += ' on {}/{} at {}'.format(times[0], times[1], times[2])
        return ret

    def _make_geo_json(self):
        return self.properties['location']
