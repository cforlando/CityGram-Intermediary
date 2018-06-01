"""
voting_centers.py - Generates a file associating precinct ID with the current voting center

Part of this script accesses OpenStreetMap and is subject to rate limitting.
We therefore only look up precinct IDs not currently found in the output.
"""

# stdlib
import random
# library
import requests
import usaddress
from bs4 import BeautifulSoup
from shapely.geometry import  shape, Point, Polygon

# Used for coord to address lookup
OSM_URL = 'https://nominatim.openstreetmap.org/reverse.php?format=json&lat={}&lon={}'

# Used for voting center lookup
AUTH_IDS = ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
FORM_URL = 'http://www.ocfelections.com/voter_lookup/FindPollingPlace.aspx'
FORM_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

def point_in_polygon(polygon: Polygon) -> Point:
    """
    Returns a random Point contained in a given Polygon
    """
    minx, miny, maxx, maxy = polygon.bounds
    point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    while not polygon.contains(point):
        point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    return point

def coord_to_addr(lat: float, lon: float) -> (str, str, str):
    """
    Uses OpenStreetMap to convert a lat/lon to address with number, street, and zipcode

    This service is subject to daily rate limitting
    """
    resp = requests.get(OSM_URL.format(lat, lon))
    if resp.status_code != 200:
        return None, None, None
    data = resp.json()
    if 'address' not in data:
        return None, None, None
    addr = data['address']
    return addr.get('house_number'), addr.get('road'), addr.get('postcode')

def extract_center(html: str) -> str:
    """
    Extracts the voting center address from a successful loopup page
    """
    soup = BeautifulSoup(html, 'html.parser')
    # 'precinct_id': soup.find(id='cntyPrctLbl').text
    center = soup.find(id='cntyPllLbl')
    if center is not None:
        return center.text
    return None

def get_form_auth(session: requests.Session) -> dict:
    """
    Pulls form validation elements from the center lookup page
    """
    response = session.get(FORM_URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    auth = {k: soup.find(id=k).get('value') for k in AUTH_IDS}
    return auth

def fetch_center(address: str, zipcode: int) -> str:
    """
    Returns the voting center for an address and zipcode
    """
    addr = usaddress.tag(address)[0]
    form = {
        'STRT_NMBR': addr['AddressNumber'],
        'drctnDDL': addr.get('StreetNamePreDirectional'),
        'StrNmeTb': addr['StreetName'],
        'ZP_CDE': str(zipcode),
        'submitBtn': 'Find Your Polling Place'
    }
    session = requests.Session()
    form.update(get_form_auth(session))
    response = session.post(FORM_URL, headers=FORM_HEADERS, data=form)
    return extract_center(response.text)

def get_center(geom: Polygon) -> (str, str):
    """
    Returns the voting center for a precinct Polygon or None if too many tries
    """
    center = None
    while center is None:
        point_times = 0
        number, street, zipcode = None, None, None
        while number is None or street is None or zipcode is None:
            coord = point_in_polygon(geom)
            print(coord.y, coord.x, end='\r')
            number, street, zipcode = coord_to_addr(coord.y, coord.x)
            point_times += 1
            if point_times > 100:
                return None
        addr = number + ' ' + street
        print('Trying Address:', addr, zipcode)
        try:
            center = fetch_center(addr, zipcode)
        except Exception as exc:
            print(exc)
    print('Got Center:', center)
    return center

def make_centers(geoms: [dict]) -> {str}:
    """
    Returns a pid: voting center dict from a list of polygon features
    """
    ret = {}
    try:
        for geom in geoms:
            pid = geom['properties']['precinct']
            print('Fetching precinct:', int(pid), '\n')
            center = get_center(shape(geom['geometry']))
            ret[pid] = center
    except requests.exceptions.ConnectionError as exc:
        print('Returning subset after connection error:', exc)
    return ret
