#!/usr/bin/python3

import argparse
import toml
import os
import sys

from getosmapsgpx import get_gpx

curl_help_str="A good firefox curl command to get an OS maps GPX file\n\
Go to firefox, perform a legitimate GPX download with the network monitor open\n\
Then right click the event, copy curl, then paste into this file"

parser = argparse.ArgumentParser(description="Look through TOML files of walks and cache all GPX", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('out_dir', metavar='O', type=str, help='Director to put output in')
parser.add_argument('curl_file', metavar='C', type=str, help=curl_help_str)
parser.add_argument('files', metavar='F', type=str, nargs='+', help='TOML file(s) to process')
args = parser.parse_args()

for file in args.files:
    config = toml.load(file)

    for name, dict in config.items():
        if "osmapsroute" in dict:
            output_filename = args.out_dir+"/"+name+".gpx"
            print(output_filename)
            if not (os.path.exists(output_filename)):
                gpx_str = get_gpx(args.curl_file, dict["osmapsroute"])
                f = open(output_filename, "w")
                f.write(gpx_str)
