""""""

from cgorl.services.voting import VotingService

_SERVICES = (
    VotingService,
)

SERVICES = {service.tag: service for service in _SERVICES}
