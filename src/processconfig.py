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

    top_name = Path(file).stem.replace("_", " ") # Use the filename for the KML folder (but with underscores replaced with spaces)

    if t["filetype"] == "walk":
        folder = kml.add_folder(output_root, top_name)
        for walk in t["walks"]:
            walk = sanitise_section_args(walk)
            # If the file is local, get it from the source directory
            # otherwise the build process will have cached it for us
            filename = "../gen/kml/"+walk["name"].replace(" ", "_")+".kml"
            gpsbabel_kml.append_gpsbabel_kml_paths_to_folder(folder, filename, walk["name"], walk["description"])
    elif t["filetype"] == "trig":
        trigdb = os_trigs.process_csv("../data/other/"+t["datasource"])
        for trig in t["trigs"]:
            # Find the corresponding trig in the database and update it
            for i in range(0, len(trigdb)):
                if trigdb[i].name == trig["name"]:
                    trigdb[i].visited = True
                    trigdb[i].user_comment = trig["description"]
                    trigdb[i].visit_dates = trig["dates"]
                    break

        visited_trigs = [t for t in trigdb if t.visited]
        if len(visited_trigs) > 0:
            folder = kml.add_folder(output_root, top_name+": Visited")
            os_trigs.add_trigs_to_tree(folder, visited_trigs)
    else:
        assert False, "Unknown file type %s" %(t["filetype"])

# Write the generated file to stdout
kml.print_tree(output_root)
