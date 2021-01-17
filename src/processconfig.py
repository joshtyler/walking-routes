#!/usr/bin/python3

import argparse
import toml
from pathlib import Path
import sys

import kml
import gpsbabel_kml
import os_trigs

def sanitise_section_args(args_dict):
    # If a description was provided use it, otherwise don't have this element
    if not "description" in args_dict:
        args_dict["description"] = None

    if not "dates" in args_dict:
        args_dict["dates"] = list()
    return args_dict

parser = argparse.ArgumentParser(description="Process TOML files of walks into one KML")
parser.add_argument('files', metavar='F', type=str, nargs='+', help='TOML file(s) to process')
args = parser.parse_args()

output_root = kml.create_root()

for file in args.files:
    t = toml.load(file)

    # Create a folder for the contents of this toml file
    # Use the filename for the KML folder (but with underscores replaced with spaces)
    folder = kml.add_folder(output_root, Path(file).stem.replace("_", " "))

    # Process all walks in file
    for name, args in t.items():
        args = sanitise_section_args(args)

        if t["filetype"] == "walk":
            # If the file is local, get it from the source directory
            # otherwise the build process will have cached it for us
            filename = "../gen/kml/"+name.replace(" ", "_")+".kml"

            # Add in the walk
            gpsbabel_kml.append_gpsbabel_kml_paths_to_folder(folder, filename, name, args["description"])
        elif t["filetype"] == "trig":
            trigs = os_trigs.process_csv(t["datasource"])
           # Filter out based on distance and add to tree with metadata here
        else:
            assert False, "Unknown file type %s" %(t["filetype"])

# Write the generated file to stdout
kml.print_output_file(output_root)
