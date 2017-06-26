Set of scripts intended to fully automate the process of finding all administrative boundary data on HDX, downloading & unzipping it, simplifying the shapfiles through Mapshaper, uploading in PostGIS database and processing them further within PostGIS.

# Setup
* Clone this repository to a local folder
* Activate the virtual environment by going to test/Scripts/ and running activate.bat (from commandline)
* Make sure mapshaper is installed using NPM: 'npm install -g mapshaper'
* Possibly install OSGeo4W (see pg_upload.bat script)

# Running scripts
Relevant scripts (in order) are:
* test/Scripts/hdx_test.py: this script searches HDX for admin-data and stores relevant info in a metadatabase tables
* get_data.py: this script uses the metadata table to actually download all the data (in folder zipfiles), and unzip them (in folder shapefiles)
* mapshaper.bat: this script simplifies all shapefiles using mapshaper (see https://github.com/mbloch/mapshaper)
* pg_upload.bat: this script uploads all shapefiles into PostGIS database. (Note that with me this didn't work in a normal terminal initially, because I didn't have a postgres driver installed for ogr2ogr. I eventually downloaded OSGeo4W and run this script from the OSGeo4W Shell. There should probably be a better way though.)
* run_sql.py: this script actually processes uploaded datatables within PostGIS. It needs column names of pcodes etc (filled in in the metadata table) to do so however.

