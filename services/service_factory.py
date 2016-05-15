from services.police_report import PoliceReport


class ServiceFactory:

    def get_service(tag):

        if tag == PoliceReport.tag:
            return PoliceReport()
        return None