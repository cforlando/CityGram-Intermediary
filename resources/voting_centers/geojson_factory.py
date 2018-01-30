"""
geojson_factory.py - Convert ArcGIS data files into a GeoJSON output
"""

# library
import begin
import shapefile
from dbfread import DBF

@begin.start
def main(input: 'Name of the files to be converted (dbf, shp)',
         output: 'Name of the output GeoJSON file' = 'output'):
    """
    Convert ArcGIS data files into a GeoJSON output

    The input files must all have the same name
    """
    # Remove the file ext
    input = '.'.join(input.split('.')[:-1])
    dbf = DBF(input + '.dbf')
    shapes = shapefile.Reader(input + '.shp').shapes()
    if len(dbf) != len(shapes):
        raise Exception('Files do not have the same number of elements')
    for meta, shape in zip(dbf, shapes):
        print(meta['PRECINCT'])
        print(shape)
        break
