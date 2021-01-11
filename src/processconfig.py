#!/usr/bin/python3

import argparse
import toml
from pathlib import Path
import sys

import processgpsbabelkml as kml

def sanitise_walk_args(args_dict):
    # If a description was provided use it, otherwise don't have this element
    if not "description" in args_dict:
        args_dict["description"] = None

    return args_dict

parser = argparse.ArgumentParser(description="Process TOML files of walks")
parser.add_argument('files', metavar='F', type=str, nargs='+', help='TOML file(s) to process')
args = parser.parse_args()

output_root = kml.create_top_level_kml()

for file in args.files:
    config = toml.load(file)

    # Create a folder for the contents of this toml file
    # Use the filename for the KML folder (but with underscores replaced with spaces)
    folder = kml.add_folder_to_kml(output_root, Path(file).stem.replace("_", " "))

    # Process all walks in file
    for name, args in config.items():
        args = sanitise_walk_args(args)

        # If the file is local, get it from the source directory
        # otherwise the build process will have cached it for us
        filename = "../gen/kml/"+name.replace(" ", "_")+".kml"

        # Add in the walk
        kml.process_kml_file(folder, filename, name, args["description"])

# Write the generated file to stdout
kml.print_output_file(output_root)
