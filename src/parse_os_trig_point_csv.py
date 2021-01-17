#!/usr/bin/python3

import argparse
import csv
from dataclasses import dataclass
from lxml import etree
import geopy.distance

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
	coords: tuple

def process_csv(file):
	trigs = []
	with open(file, newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['TYPE OF MARK'] == 'PILLAR':
				longlat = ENtoLL84(row['EASTING'], row['NORTHING'])
				destroyed = False
				if row['DESTROYED MARK INDICATOR'] != '0':
					destroyed = True
				trigs.append(Trig(row['Trig Name'], row['HEIGHT'], destroyed, row['COMMENTS'], longlat))

	return trigs

# Annoyingly KML files have the default namespace set to this
# This is a bit of a pain to parse in lxml, but oh well...
kml_default_namespace="http://www.opengis.net/kml/2.2"
ns = {"kml":kml_default_namespace}

def write_kml(trigs):
	# Create xml tree
	root =  etree.Element("kml", nsmap={None: kml_default_namespace})

	# Add a folder
	folder = etree.SubElement(root, "Folder")
	name_element = etree.SubElement(folder,"name")
	name_element.text = "Trigs"

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
		coords.text = "%s,%s"%(trig.coords)

	print(etree.tostring(root, pretty_print=True, encoding='unicode'))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse the OS trig point database")
	parser.add_argument('file', metavar='C', type=str, help='Trig point CSV file')
	args = parser.parse_args()
	trigs = process_csv(args.file)

	trigs = [t for t in trigs if geopy.distance.distance(geopy.distance.lonlat(t.coords[0],t.coords[1]), geopy.distance.lonlat(-0.584897, 51.237755)).miles < 15]
	write_kml(trigs)
