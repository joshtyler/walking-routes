#!/usr/bin/python3

import argparse
import toml
from pathlib import Path
import sys

import processgpsbabelkml as kml

parser = argparse.ArgumentParser(description="Process a TOML file of walks")
parser.add_argument('files', metavar='F', type=str, nargs='+', help='TOML file to process')
args = parser.parse_args()

for file in args.files:
    folder_name = Path(file).stem # Use the filename for the KML folder
    config = toml.load(file)
    sys.stderr.write(str(config))
    output_root = kml.create_top_level_kml()
    folder = kml.add_folder_to_kml(output_root, folder_name)
    for name, args in config.items():
        sys.stderr.write(str(name))
        sys.stderr.write("\n")
        sys.stderr.write(str(args))
        sys.stderr.write("\n\n")
        description = None
        if "description" in args:
            description = args["description"]
        kml.process_kml_file(folder, "../gen/kml/"+args["source_filename"]+".kml", name, description)
        kml.print_output_file(output_root)
