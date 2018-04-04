"""
geojson_factory.py - Convert ArcGIS data files into a GeoJSON output

Ex: python geojson_factory.py precinct_files/May2016Precinct_region.shp
"""

# stdlib
import json
# library
import begin
import shapefile
from dbfread import DBF

@begin.subcommand
def geoms(input: 'Name of the files to be converted (dbf, shp)',
          output: 'Name of the output GeoJSON file' = 'geometries'):
    """
    Convert ArcGIS data files into a GeoJSON output

    The input files must all have the same name
    """
    # Remove the file ext
    input = '.'.join(input.split('.')[:-1])
    # Import meta data and shapes
    dbf = DBF(input + '.dbf')
    shapes = shapefile.Reader(input + '.shp').shapes()
    if len(dbf) != len(shapes):
        raise Exception('Files do not have the same number of elements')
    # Format shape files into an ID key dict of GeoJSON objects
    features = []
    for meta, shape in zip(dbf, shapes):
        if shape.shapeType == shapefile.POLYGONZ:
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [shape.points]
                },
                'properties': {k.lower(): v for k, v in meta.items()}
            })
    # Export as a JSON file
    json.dump({
        'type': 'FeatureCollection',
        'features': features
    }, open(output + '.geojson', 'w'))

@begin.subcommand
def voting(centers: 'Voting centers file path',
           dates: 'Election dates file path',
           geoms: 'Geometry file path') -> int:
    """
    Generate master output from voter center, election date, and precinct geometries data files

    The output is placed into a publically-callable place for Citygram to pull from like S3
    """
    centers, dates, geoms = [json.load(open(path)) for path in (centers, dates, geoms)]
    print(dates)
    return 0

@begin.start
def main():
    pass
