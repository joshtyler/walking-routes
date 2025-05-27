#!/bin/bash
set -e

if [[ $# -lt 1 ]]; then
	echo "Take file(s) and convert to a single KML file"
	echo "Usage: $0 [Input FILE 0] ..."
	echo "(KML file is output to standard output)"
	exit 1
fi

INPUT_STR=""
for var in "$@"; do
	# Get extension as all lowercase
	EXTENSION=$(basename ${var}) # Get just the filename
	EXTENSION=${EXTENSION##*.} # Nab the extension
	EXTENSION=${EXTENSION,,} # Convert to lowercase
	TYPESTR=""
	case ${EXTENSION} in
		"gpx")
			TYPESTR="gpx"
			;;
		"fit")
			TYPESTR="garmin_fit"
			;;
		*)
			echo "Unknown file type ${EXTENSION}"
			exit 1
	esac

	INPUT_STR+="-i ${TYPESTR} -f ${var} "
done


# Merge gaps in input tracks
# remove waypoints
gpsbabel ${INPUT_STR} -x track,merge -o kml,points=0 -F -
