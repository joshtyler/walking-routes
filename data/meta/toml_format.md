# Format of TOML files
This directory contains TOML files that are used to build the generated KML. Each TOML file turns into a folder in the generated KML.

Files are identified by the the ```filetype="type"``` identifier at the top of the file.

Supported types are:
* ```walk``` (For walks)
* ```trig``` (For trigpoints)

## Properties Applying to all types
* Filenames map to Human readable names but with spaces swapped for underscores
	* This is to allow the Makefile to work correctly.
		* ```wildcard``` etc. does not play nicely with spaces :disappointed:
	* E.g. ```["My Walk"]``` could map to ```My_Walk.gpx```
	* E.g. ```Trig_Pillars.toml``` creates a KML folder called ```Trig Pillars```
* Sub-properties on each section:
	* ```description``` (optional): Used to populate the path/point description in the KML (other auto-generated info is appended too)
	* ```dates``` (optional): Array of date(s) walked/visited

## Walks
* Each TOML section is a different walk
* The section title is the title of the walk
* One of a number of properties is set to show that the source file is fetched from a remote source
	* From osmaps.ordnancesurvey.co.uk : ```osmapsid="xxxx"```.
		* ```xxxx``` is the ID of the walk. I.e. The ```xxxx``` in this URL template ```https://osmaps.ordnancesurvey.co.uk/route/xxxx/yyyy```
	* (Currently OS maps is the only supported remote source)
* If no source is given, it is assumed that the file is local and stored in the data directory.
	* It must be named the same as the walk title (but with spaces/underscores exchanged, see above)

Example:
``` toml
filetype="walk"
["My Walk"]
dates= 2000-01-01
description="""
Very muddy
"""
osmapsid="123456" # If missing assumed to be local file called "My_Walk.xxx"
```

## Trigpoints
* The following global settings must be present:
	* ```datasource="filename.csv"```
		* Stored in the ```data/other``` folder.
		* Assumed to be the same format as from [the OS website](https://www.ordnancesurvey.co.uk/gps/legacy-control-information/triangulation-stations)
* The following global settings can be optionally included:
	* ```include = [["Buckingham Palace" 51.5014, -0.1419, 100]]```
		* This is an array of locations to include trig points around
		* Each array element is ```[name, latitude, longitude, distance]```
			* Name is the name of the location
			* latitude, longitude are the co-ordinates of the location
			* distance is the distance in **miles** to include around this location
		* The example includes all trig points within 100 miles of Buckingham Palace
* Each section represents a visited trig (Name must match the CSV)
* The trig points in the generated KML file are:
	* All visited pillars
	* All pillars included above
* We don't include all pillars by default because the KML file becomes too large for Google Maps to handle (it limits to 1000 points (per folder?))

Example:
``` toml
filetype="trig"
datasource="osdata.csv"
include = [["Buckingham Palace" 51.5014, -0.1419, 100]]
["Ben Nevis"]
dates= 2000-01-01
description="""
Great views!
"""
```
