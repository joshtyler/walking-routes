#!/usr/bin/python3

import argparse
import csv
from dataclasses import dataclass

import geopy.distance
import import collections.namedtuple

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

Coords = namedtuple("Coords", "lat long")

@dataclass
class Trig:
	name: str
	height : float
	destroyed : bool
	os_comment : str
	coords: Coords

def process_csv(file):
	trigs = []
	with open(file, newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['TYPE OF MARK'] == 'PILLAR':
				longlat = ENtoLL84(row['EASTING'], row['NORTHING'])
				coords = Coords(longlat[1], longlat[0])
				destroyed = False
				if row['DESTROYED MARK INDICATOR'] != '0':
					destroyed = True
				trigs.append(Trig(row['Trig Name'], row['HEIGHT'], destroyed, row['COMMENTS'], coords))

	return trigs

def write_kml(trigs):
	# Create xml tree
	root = kml_writer.create_root()

	# Add a folder
	folder = kml_writer.add_folder(root, "Trigs")

	for trig in trigs:
		mark = etree.SubElement(folder, "Placemark")

		name = etree.SubElement(mark, "name")
		name.text = trig.name

		desc = etree.SubElement(mark, "description")
		str = "Height: %s" %(trig.height)
		if trig.destroyed:
			str = str + "\nMarked as destroyed."
		if trig.os_comment and (not trig.os_comment.isspace()):
			str = str + "\nOS Comment: %s" %(trig.os_comment)

		desc.text = str

		point = etree.SubElement(mark, "Point")
		coords = etree.SubElement(point, "coordinates")
		coords.text = "%s,%s"%(trig.coords.long, trig.coords.lat)

	print(etree.tostring(root, pretty_print=True, encoding='unicode'))

def distance_from_trig(coords):
	geopy.distance.distance(geopy.distance.lonlat(t.coords[1],t.coords[0]), geopy.distance.lonlat(coords[1], coords[0]))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse the OS trig point database")
	parser.add_argument('file', metavar='C', type=str, help='Trig point CSV file')
	args = parser.parse_args()
	trigs = process_csv(args.file)

	write_kml(trigs)
