#!/usr/bin/python3
from lxml import etree
from collections import namedtuple

# Functions to create a KML file

# Annoyingly KML files have the default namespace set to this
# This is a bit of a pain to parse in lxml, but oh well...
kml_default_namespace="http://www.opengis.net/kml/2.2"
ns = {"kml":kml_default_namespace}

Coord = namedtuple("Coord", "lat lon")

def create_root():
    return etree.Element("kml", nsmap={None: kml_default_namespace})

def get_root_from_file(filename):
    return etree.parse(filename).getroot()

def get_parent(tree):
    return tree.find("./..")

def get_name(node):
    # In KML nodes sometimes have a subnode called name
    # The value of this is the name of the thing
    name = None
    name_elem = node.find("kml:name",ns)
    if name_elem is not None:
        name = name_elem.text
    return name

def get_all_paths(node):
    return node.findall(".//kml:LineString",ns)

def contains_path(node):
    return len(get_all_paths(node)) > 0

def get_coordinates_of_path(linestring):
    coordinates = linestring.find("./kml:coordinates",ns).text.split()
    coordinates = [c.split(',') for c in coordinates if not c.isspace()] # Remove whitespace
    coordinates = [Coord(float(c[1]),float(c[0])) for c in coordinates] # Convert to Coords tuple (N.B. Order reversal)
    return coordinates

def set_name(node, name):
    # Set the name subelement either by overwriting, or creating it
    name_node = node.find("kml:name",ns)
    if name_node is None:
        name_node = add_subelement(node, "name")
    name_node.text = name

def set_description(node, desc):
    # Set the descripton subelement either by overwriting, or creating it
    descripton_node = node.find("kml:descripton",ns)
    if descripton_node is None:
        descripton_node = add_subelement(node, "descripton")
    descripton_node.text = desc

def get_placemarks(tree):
    # Going from the root, as provided by gpsbabel, they match this xpath
    #"./kml:Document/kml:Folder/kml:Folder"
    return tree.findall(".//kml:Placemark", ns)

def add_subelement(parent, name, text=None):
    subelem = etree.SubElement(parent, name)
    if text is not None:
        subelem.text = text
    return subelem

def add_folder(parent, name):
    folder = add_subelement(parent,"Folder")
    add_subelement(folder, "name", name)
    return folder

def add_point(node, coord):
    point_node = etree.SubElement(node, "Point")
    coord_node = etree.SubElement(point_node, "coordinates")
    coord_node.text = "%.6f,%.6f"%(coord.lon, coord.lat)

def print_tree(root):
	print(etree.tostring(root, pretty_print=True, encoding='unicode'))

def write_tree(root, filename):
    etree.ElementTree(root).write(filename, xml_declaration=True, encoding='UTF-8', pretty_print=True)

def add_placemark(parent, name):
    node = add_subelement(parent, "Placemark")
    if name is not None:
        set_name(node,name)
    return node
