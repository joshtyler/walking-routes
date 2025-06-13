#!/usr/bin/python3

import csv
import sys
import geojson

from pathlib import Path
this_dir = Path(__file__).parent.absolute()

# From https://webscraping.com/blog/Converting-UK-Easting-Northing-coordinates/
from pyproj import Proj, transform
v84 = Proj(proj="latlong",towgs84="0,0,0",ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy",
	towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894")
vgrid = Proj(init="world:bng")

def ENtoLL84(easting, northing):
	"""Returns (longitude, latitude) tuple
	"""
	vlon36, vlat36 = vgrid(easting, northing, inverse=True)
	return transform(v36, v84, vlon36, vlat36)
# End code from https://webscraping.com/blog/Converting-UK-Easting-Northing-coordinates/


def get_trigs_geojson():
	file = this_dir / "CompleteTrigArchive.csv"
	trigs = []
	with open(str(file), newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['TYPE OF MARK'] == 'PILLAR':
				longlat = ENtoLL84(row['EASTING'], row['NORTHING'])
				coord = geojson.Point((longlat[0], longlat[1]))
				properties = {
					"name" : row['Trig Name'],
					"height" : row['HEIGHT'],
					"destroyed" : (row['DESTROYED MARK INDICATOR'] != '0'),
					"os_comment" : row['COMMENTS'],
				}
				if not properties["destroyed"]:
					trigs.append(geojson.Feature(geometry=coord,properties=properties))
	return geojson.FeatureCollection(trigs)

def trigs_geojson_to_file(filename):
	with open(filename, "w") as f:
		j = get_trigs_geojson()
		geojson.dump(j,f)

if __name__ == "__main__":
	name = "test.json"
	if len(sys.argv) >= 2:
		name = sys.argv[1]
	trigs_geojson_to_file(name)
