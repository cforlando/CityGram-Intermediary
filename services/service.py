# -- Michael duPont
# -- Fetch data from a "near real time" JSON data source, format to
# -- be Citygram compliant, and print the list of JSON objects
# -- 2016-04-17

import hashlib
import abc
from datetime import datetime, timedelta


class Service(metaclass=abc.ABCMeta):
    """ Service parent class definition """

    # Static Class Members
    tag = None  # Static member to identify the service.
    req_keys = None  # Required Keys
    url = None  # Base url
    time_window = 720  # Number of minutes for the timeframe

    @staticmethod
    def get_timestamp(minago, strf):
        """ Returns a strf formatted timestamp a given number of minutes prior to 'now' """

        retTime = datetime.now() - timedelta(minutes=minago)
        return retTime.strftime(strf)

    def __init__(self):
        """ Class init """
        self.properties = None
        self.id = ''
        self.geojson = {}

    # The next two require child-specific implementation
    @abc.abstractmethod
    def _make_title(self):
        """ Returns a string fully describing the alert/event """
        return ''

    @abc.abstractmethod
    def _make_geo_json(self):
        """ Returns a Citygram-compliant geometry dictionary """
        return {}

    def _check_for_keys(self, keylist=None):
        """
        :param keylist: list
        :return: True if all given keys are in properties
        """
        if keylist is None:
            keylist = self.__class__.req_keys

        for item in keylist:
            if item not in self.properties: return False
            elif self.properties[item] in ['', 'NULL']: return False
        return True

    def _filter(self):
        """ Child classes have the option to filter objects.
        Filter fields should be included in requiredKeys
        :return: True if an object is to be included in the features list
        """
        return True

    def _validate(self):
        """ Returns True if object passes all validation tests """
        try:
            assert('title' in self.properties)  # A title has been set in the properties dict
            assert(type(self.id) == str)        # The id is a string
            assert(self.id != '')               # The id has been changed
            assert(type(self.geojson) == dict)  # The geoLoc is a dict
            assert(self.geojson != {})          # The geoLoc has been changed
            return True
        except: return False
    
    def _update(self):
        """ Formats and sets required data fields and runs verification
        :return: True if successful, else False
        """
        try:
            title = self._make_title()
            self.properties['title'] = title
            self.set_id(title)
            self.geojson = self._make_geo_json()
            return self._validate()
        except Exception as e:
            return False
    
    def _export(self):
        """ Returns a Citygram-compliant version of the original object
        :return: json obj
        """
        return {
            'id': self.id,
            'type': 'Feature',
            'geometry': self.geojson,
            'properties': self.properties
        }

    def set_id(self, inc_string):
        """ Set the object id to be equal to the SHA-1 hex value of a string
        :param inc_string:
        """
        hasher = hashlib.sha1()
        # Remove non-ascii chars for hash
        hasher.update((''.join(i for i in inc_string if ord(i) < 128)).encode('utf-8'))
        self.id = hasher.hexdigest()

    def get_url(self):
        """ Getter for the url. Currently returns the base url defined in the subclass
        :return: str
        """
        return self.__class__.url + ('$where=when > "{}"'.format(Service.get_timestamp(self.__class__.time_window,
                                                                             '%Y-%m-%dT%H:%M:%d')))

    def process_object(self, item):
        """ Performs the processing on the object to be exported
        :param item: json obj to be parsed
        :return: json object to be exported.
        """
        # If original object contains all the required keys and their values are not null
        # And the data passes the service's filter
        self.properties = item
        if self._check_for_keys() and self._filter():
            # If the new object updates and passes validation
            if self._update():
                return self._export()

        return None
