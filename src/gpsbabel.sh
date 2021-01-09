#!/bin/bash
gpsbabel -i gpx -f 20210109-Gomshall.gpx -f woking.gpx -o kml,points=0 -F kmltest.kml
