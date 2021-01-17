#!/usr/bin/python3

import argparse
from lxml import etree
import kml
import sys


# The structure of the gpsbabel generated docuemnt is:
# Folder (name="Routes")
# 	Folder (name=**route_name1**)
#		Placemark (name="Path") [data is here]
# 	Folder (name=**route_name2**)
#		Placemark (name="Path") [data is here]

# Take a gpsbabel KML file of paths, extract the path data, and append to a different folder
def append_gpsbabel_kml_paths_to_folder(folder, file, name=None, description=None):
	# Parse our input generated by gpsbabel as an element tree
	root = kml.get_root_from_file(file)
	marks = kml.get_placemarks(root)

	marks = [m for m in marks if kml.contains_path(m)]

	# Expect only one Placemark if the name is provided
	if name is not None:
		assert(len(marks) == 1)

	for item in marks:
		# GPS Babel gives the containing folder the route name
		parent_name = kml.get_name(kml.get_parent(item))
		if parent_name == None:
			parent_name = "[Unnamed]"

		print("Found a route in a folder named: %s" %(parent_name), file=sys.stderr)

		# Set the placemark name correctly
		# Prefer to use the name given to us, but otherwise fall back to what is embedded in the file
		if name is None:
			name = parent_name
		kml.set_name(item,name)

		# Set description if we have one
		if description is not None:
			kml.set_description(item, description)

		# Remove style data that gpsbabel adds in
		item.remove(item.find("kml:styleUrl",kml.ns))

		# Append this to the output
		folder.append(item)
	return folder



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""\
	Take one or more KML files generated by gpsbabel
	Extract the bits we are interested in
	Write them to a clean KML file (output to stdout)\
	""")
	parser.add_argument('files', metavar='F', type=str, nargs='+', help='gpsbabel KML files to process')
	args = parser.parse_args()

	root = kml.create_root()
	folder = kml.add_folder(root, "Walks")

	for file in args.files:
		append_gpsbabel_kml_paths_to_folder(folder, file)
	kml.print_tree(root)
