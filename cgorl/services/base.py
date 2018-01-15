""""""

# stdlib
import hashlib

class Service(object):
    """
    Service base class
    """

    tag: str = None
    id: str = None
    properties: dict = None
    geojson: dict = None

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

    def _filter(self):
        """
        Child classes have the option to filter objects.

        Filter fields should be included in required_keys

        Returns True if an object is to be included in the features list
        """
        return True

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
            # The geoLoc is a dict
            assert isinstance(self.geojson, dict)
            # The geoLoc has been changed
            assert len(self.geojson) > 0
            return True
        except:
            return False

    def _export(self) -> {str: object}:
        """
        Returns a Citygram-compliant, JSON-compatible dictionary of the original object
        """
        return {
            'id': self.id,
            'type': 'Feature',
            'geometry': self.geojson,
            'properties': self.properties
        }

class PointService(Service):
    """
    Services deriving from Point geometries
    """
    pass

class PolygonService(Service):
    """
    Services deriving from Polygon geometries
    """
    pass
