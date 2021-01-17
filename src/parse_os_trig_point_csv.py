#!/usr/bin/python3

import argparse
import csv
from dataclasses import dataclass

import geopy.distance
from collections import namedtuple
import kml

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

@dataclass
class Trig:
	name: str
	height : float
	destroyed : bool
	os_comment : str
	coord: kml.Coord

def process_csv(file):
	trigs = []
	with open(file, newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['TYPE OF MARK'] == 'PILLAR':
				longlat = ENtoLL84(row['EASTING'], row['NORTHING'])
				coord = kml.Coord(longlat[1], longlat[0])
				destroyed = False
				if row['DESTROYED MARK INDICATOR'] != '0':
					destroyed = True
				trigs.append(Trig(row['Trig Name'], row['HEIGHT'], destroyed, row['COMMENTS'], coord))

	return trigs

def add_trigs_to_tree(folder, trigs):

	for trig in trigs:
		mark = kml.add_placemark(folder, trig.name)

		str = "Height: %s" %(trig.height)
		if trig.destroyed:
			str = str + "\nMarked as destroyed."
		if trig.os_comment and (not trig.os_comment.isspace()):
			str = str + "\nOS Comment: %s" %(trig.os_comment)

		kml.set_description(mark, str)
		folder.append(mark)
	return folder


def distance_from_trig(coords):
	geopy.distance.distance(geopy.distance.lonlat(t.coord.lon,t.coord.lat), geopy.distance.lonlat(coord.lon, coord.lat))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse the OS trig point database")
	parser.add_argument('file', metavar='C', type=str, help='Trig point CSV file')
	args = parser.parse_args()
	trigs = process_csv(args.file)

	root = kml.create_root()
	folder = kml.add_folder(root, "Trigs")
	folder = add_trigs_to_tree(folder, trigs)
	kml.print_tree(folder)
