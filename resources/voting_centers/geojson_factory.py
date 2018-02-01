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

@begin.start
def main(input: 'Name of the files to be converted (dbf, shp)',
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
