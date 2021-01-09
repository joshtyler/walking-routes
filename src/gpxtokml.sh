#!/bin/bash
set -e

if [[ $# -lt 1 ]]; then
	echo "Take GPX file(s) and convert to a KML file"
	echo "Usage: $0 [GPX FILE 0] ..."
	echo "(KML file is output to standard output)"
	exit 1
fi

INPUT_STR=""
for var in "$@"; do
	INPUT_STR+="-f ${var} "
done


gpsbabel -i gpx ${INPUT_STR} -o kml,points=0 -F -
