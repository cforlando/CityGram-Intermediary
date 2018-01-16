""""""

from cgorl.services.base import PolygonObject, Service

class VotingObject(PolygonObject):
    """
    """

    pass

class VotingService(Service):
    """
    Time-based service for voting center notifications
    """

    tag = 'voting'
    data_source = ''
    service_object = VotingObject

    def _filter(self, data: dict) -> bool:
        """
        """
        return True
