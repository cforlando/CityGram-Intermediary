# Voting Centers Resources

Code, data, and resources for building the source file for Orlando voting notifications

## Getting Started

This sub-project uses a Python command line utility to process raw data files. You'll need Python3 installed (preferably always the most recent minor version). You should activate a virtual env, but it's not the end of the world. Install the dependacies:

```python
cd voting_centers
pip install -r requirements.txt
```

The command line utility has built-in help docs and is callable like so:

```bash
python factory.py -h
```

## Precinct Geometries

Creates the geojson file from [Orange County precinct GIS files](http://www.ocfelections.com/PrecinctGISFiles.aspx)

```bash
python factory.py geoms resources/precinct_files/May2016Precinct_region.shp
```

The output is a feature collection of polygons. As a sanity check, the [rendered precinct geojson data](https://github.com/cforlando/CityGram-Intermediary/blob/master/voting_centers/data/geometries.geojson) can be viewed on GitHub

## Election Dates

Orange County major elections calendar - [link](http://www.ocfelections.com/Election_Calendar.aspx)

## Voting Centers
