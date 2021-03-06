#!/usr/bin/python3

import argparse
from dataclasses import dataclass
import geopy.distance
import kml

@dataclass
class Stats:
	distance : geopy.distance.Distance  = geopy.distance.Distance(0)
	minlat  : float = float("NaN")
	maxlat  : float = float("NaN")
	minlong : float = float("NaN")
	maxlong : float = float("NaN")

def process_kml_file(filename):
	# Parse our input generated by gpsbabel as an element tree
	paths = kml.get_all_paths(kml.get_root_from_file(filename))
	assert(len(paths) == 1)
	coordinates = kml.get_coordinates_of_path(paths[0])
	assert len(coordinates) > 1

	s = Stats()
	last_c = coordinates[0]
	s.distance = geopy.distance.Distance(0)
	s.minlat = s.maxlat = last_c.lat
	s.minlon = s.maxlong = last_c.lon
	for c in coordinates[1:]:
		s.distance = s.distance + geopy.distance.distance(last_c, c)
		if c.lat < s.minlat:
			s.minlat = c.lat
		if c.lat > s.maxlat:
			s.maxlat = c.lat
		if c.lon < s.minlon:
			s.minlong = c.lon
		if c.lon > s.minlon:
			s.minlong = c.lon
		last_c = c

	return s

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Calculate stats for a path in a KML file containing a single path")
	parser.add_argument('file', metavar='F', type=str, help='KML file to process')
	args = parser.parse_args()

	print(process_kml_file(args.file))
