""""""

# stdlib
import hashlib
import json
# library
import requests

class ServiceObject(object):
    """
    Base service object class
    """

    id: str = None
    properties: dict = None
    geojson: dict = None

    def __init__(self, data: dict):
        self.properties = {}
        self.geojson = {}
        self.valid = self.process(data)

    def _make_title(self) -> str:
        """
        Returns a user-readable string fully describing the alert/event
        """
        raise NotImplementedError()

    def _make_geojson(self) -> dict:
        """
        Returns a Citygram-compliant geometry dictionary
        """
        raise NotImplementedError()

    def set_id(self, title: str):
        """
        Set the object id to be equal to the SHA-1 hex value of a string
        """
        hasher = hashlib.sha1()
        # Remove non-ascii chars for hash
        hasher.update((''.join(i for i in title if ord(i) < 128)).encode('utf-8'))
        self.id = hasher.hexdigest()

    def _validate(self):
        """
        Returns True if object passes all validation tests
        """
        try:
            # A title has been set in the properties dict
            assert 'title' in self.properties
            # The id is a string
            assert isinstance(self.id, str)
            # The id has been changed and not empty
            assert bool(self.id)
            # The geom is a dict
            assert isinstance(self.geojson, dict)
            # The geom has been changed
            assert len(self.geojson) > 0
            return True
        except:
            return False

    def process(self, data: dict) -> bool:
        """
        Processes an object and returns True if the result passes validation
        """
        title = self._make_title()
        self.properties['title']
        self.set_id(title)
        return self._validate()

    def export(self) -> {str: object}:
        """
        Returns a Citygram-compliant, JSON-compatible dictionary of the original object
        """
        return {
            'id': self.id,
            'type': 'Feature',
            'geometry': self.geojson,
            'properties': self.properties
        }

class PointObject(ServiceObject):
    """
    Services deriving from Point geometries
    """
    pass

class PolygonObject(ServiceObject):
    """
    Services deriving from Polygon geometries
    """
    pass

class Service(object):
    """
    Service base class
    """

    # Unique tag to identify the service URL
    tag: str = None

    # JSON data source. Can be a URL or file path
    data_source: str = None

    # Service object to parse raw data
    service_obj: ServiceObject = None

    def _filter(self, data: dict) -> bool:
        """
        Child classes have the option to filter objects

        Returns True if an object is to be included in the features list
        """
        return True

    def fetch(self) -> [dict]:
        """
        Retruns filtered data from a URL or file JSON data source

        Child classes should implement their own if reading from a non-JSON source
        """
        if self.data_source.startswith('http'):
            data = requests.get(self.data_source).json()
        else:
            data = json.load(open(self.data_source, 'r'))
        return [item for item in data if self._filter(item)]

    def format(self, data: [dict]) -> [dict]:
        """
        """
        objs = [self.service_obj(item) for item in data]
        return [obj.export() for obj in objs if obj.valid]
