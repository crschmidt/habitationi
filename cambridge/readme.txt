Scripts to create a geojson file of parcels with attributes from the assessment
data.

* Loads data into a sqlite3 database
** Data is grouped by the Map/Lot to combine all information about a parcel
* Imports parcel data
* Joins the tables based on Map/Lot // GIS ID
* Exports a parcels JSON file.

Requires:

 - gdal tools (sudo apt-get install gdal-bin)
 - fiona + shapely

To install fiona + shapely in a virtualenv:

  $ virtualenv env
  $ source env/bin/activate
  $ pip install -r requirements.txt


