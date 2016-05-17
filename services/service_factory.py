# -- Michael duPont
# -- Fetch data from a "near real time" JSON data source, format to
# -- be Citygram compliant, and print the list of JSON objects
# -- 2016-04-17

from services.police_report import PoliceReport


class ServiceFactory:
    """ Simple Factory Class for Services. """

    def get_service(tag):

        if tag == PoliceReport.tag:
            return PoliceReport()
        return None
